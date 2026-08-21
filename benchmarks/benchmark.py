"""Measure real Terraform apply/destroy cycles against a local Kumo runtime."""

from __future__ import annotations

import argparse
import json
import os
import platform
import socket
import statistics
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters/kumo"
FIXTURE = ROOT / "fixtures/kumo-baseline.tfvars.json"
DEFAULT_OUTPUT = ROOT / "benchmarks/results/27-kumo-provisioning-v1.json"
EXPECTED_RESOURCES = 4
UTC = timezone.utc


def checked(command: list[str], *, cwd: Path = ADAPTER) -> str:
    environment = os.environ.copy()
    environment.update(
        {
            "AWS_EC2_METADATA_DISABLED": "true",
            "TF_IN_AUTOMATION": "1",
        }
    )
    result = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        raise subprocess.CalledProcessError(result.returncode, command)
    return result.stdout


def terraform(*arguments: str) -> list[str]:
    return ["terraform", f"-chdir={ADAPTER}", *arguments]


def wait_for_port(process: subprocess.Popen[str], timeout_seconds: float = 10.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Kumo exited before readiness with code {process.returncode}")
        try:
            with socket.create_connection(("127.0.0.1", 4566), timeout=0.2):
                return
        except OSError:
            time.sleep(0.05)
    raise TimeoutError("Kumo did not listen on 127.0.0.1:4566 within 10 seconds")


@contextmanager
def kumo_runtime() -> Iterator[None]:
    binary = os.environ.get("KUMO_BIN", "kumo")
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as log:
        process = subprocess.Popen(
            [binary, "--host", "127.0.0.1", "--port", "4566"],
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
        )
        try:
            wait_for_port(process)
            yield
        except Exception:
            log.seek(0)
            lines = log.readlines()
            print("".join(lines[-40:]), file=sys.stderr)
            raise
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


def timed(command: list[str]) -> float:
    started = time.perf_counter()
    checked(command)
    return time.perf_counter() - started


def cycle() -> tuple[float, float, int]:
    common = [
        f"-var-file={FIXTURE}",
        "-input=false",
        "-no-color",
        "-auto-approve",
    ]
    apply_seconds = timed(terraform("apply", *common))
    resources = [
        line
        for line in checked(terraform("state", "list")).splitlines()
        if line.strip()
    ]
    outputs = json.loads(checked(terraform("output", "-json")))
    if len(resources) != EXPECTED_RESOURCES:
        raise RuntimeError(
            f"expected {EXPECTED_RESOURCES} resources after apply, found {len(resources)}"
        )
    if outputs["adapter"]["value"] != "kumo":
        raise RuntimeError("Terraform outputs do not identify the Kumo adapter")
    destroy_seconds = timed(terraform("destroy", *common))
    remaining = checked(terraform("state", "list")).strip()
    if remaining:
        raise RuntimeError("Terraform state is not empty after destroy")
    return apply_seconds, destroy_seconds, len(resources)


def version(command: list[str]) -> str:
    return checked(command, cwd=ROOT).splitlines()[0].strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.repeat < 1 or args.warmup < 0:
        parser.error("--repeat must be positive and --warmup cannot be negative")

    started_at = datetime.now(UTC)
    started = time.perf_counter()
    checked(terraform("init", "-backend=false", "-input=false", "-no-color"))
    apply_samples: list[float] = []
    destroy_samples: list[float] = []
    resource_counts: list[int] = []
    state_paths = [ADAPTER / "terraform.tfstate", ADAPTER / "terraform.tfstate.backup"]
    for state_path in state_paths:
        state_path.unlink(missing_ok=True)
    with kumo_runtime():
        for index in range(args.warmup):
            cycle()
        for index in range(args.repeat):
            apply_seconds, destroy_seconds, resource_count = cycle()
            apply_samples.append(apply_seconds)
            destroy_samples.append(destroy_seconds)
            resource_counts.append(resource_count)
    for state_path in state_paths:
        state_path.unlink(missing_ok=True)

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "fixture_version": "2.0.0",
        "project": "terraform-aws-baseline",
        "metric": "kumo_apply_seconds",
        "value": statistics.median(apply_samples),
        "unit": "seconds",
        "timestamp": started_at.isoformat().replace("+00:00", "Z"),
        "command": (
            f"docker run --rm terraform-aws-baseline benchmark --repeat {args.repeat} "
            "--output /output/27-kumo-provisioning-v1.json"
        ),
        "repeat": args.repeat,
        "warmup": args.warmup,
        "samples": apply_samples,
        "metrics": {
            "destroy_seconds": destroy_samples,
            "resource_parity": [count / EXPECTED_RESOURCES for count in resource_counts],
        },
        "summary": {
            "apply_min_seconds": min(apply_samples),
            "apply_median_seconds": statistics.median(apply_samples),
            "apply_max_seconds": max(apply_samples),
            "destroy_median_seconds": statistics.median(destroy_samples),
        },
        "execution": {
            "duration_seconds": time.perf_counter() - started,
            "failures": 0,
        },
        "environment": {
            "os": platform.platform(),
            "architecture": platform.machine().lower(),
            "python": platform.python_version(),
            "terraform": version(["terraform", "version"]),
            "kumo": os.environ.get("KUMO_VERSION", "unknown"),
            "aws_provider": "5.100.0",
            "adapter": "kumo",
            "aws_credentials_required": False,
        },
        "operations": {
            "resources_per_apply": EXPECTED_RESOURCES,
            "resource_counts": resource_counts,
            "apply_cycles": args.repeat,
            "destroy_cycles": args.repeat,
        },
        "compatibility_diagnostics": {
            "kumo_used": True,
            "aws_provider_loaded": True,
            "shared_module_with_aws": True,
            "aws_conformance_claim": False,
        },
    }
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
