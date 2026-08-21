"""Build the image and produce source-locked V1/V2 benchmark evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import statistics
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V1_PATH = ROOT / "benchmarks/results/27-kumo-provisioning-v1.json"
V2_PATH = ROOT / "benchmarks/publication/27-kumo-provisioning-v2.json"
SOURCE_PATHS = [
    "Dockerfile",
    "requirements.txt",
    "fixtures/kumo-baseline.tfvars.json",
    "adapters/kumo/main.tf",
    "adapters/kumo/outputs.tf",
    "adapters/kumo/provider.tf",
    "adapters/kumo/variables.tf",
    "adapters/kumo/versions.tf",
    "adapters/aws/main.tf",
    "adapters/aws/outputs.tf",
    "adapters/aws/variables.tf",
    "adapters/aws/versions.tf",
    "modules/application-baseline/main.tf",
    "modules/application-baseline/outputs.tf",
    "modules/application-baseline/variables.tf",
    "benchmarks/benchmark.py",
]
LOCK_PATHS = [
    "Dockerfile",
    "requirements.txt",
    "adapters/kumo/.terraform.lock.hcl",
    "adapters/aws/.terraform.lock.hcl",
]
UTC = timezone.utc


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def combined_digest(paths: list[str]) -> str:
    value = hashlib.sha256()
    for relative in paths:
        value.update(relative.encode("utf-8"))
        value.update(b"\0")
        value.update((ROOT / relative).read_bytes())
        value.update(b"\0")
    return "sha256:" + value.hexdigest()


def git(*arguments: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *arguments], text=True
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default="terraform-aws-baseline:local")
    parser.add_argument(
        "--producer", choices=("local", "github-actions", "other-ci"), default="local"
    )
    parser.add_argument("--ci-run-url")
    parser.add_argument("--skip-build", action="store_true")
    args = parser.parse_args()
    if args.producer != "local" and not args.ci_run_url:
        raise SystemExit("--ci-run-url is required for a non-local producer")
    if git("status", "--porcelain"):
        raise SystemExit("benchmark production requires a clean source tree")

    source_commit = git("rev-parse", "HEAD")
    if not args.skip_build:
        subprocess.run(
            ["docker", "build", "-t", args.image, "."], cwd=ROOT, check=True
        )
    image_id = subprocess.check_output(
        ["docker", "image", "inspect", "--format", "{{.Id}}", args.image], text=True
    ).strip()
    if not image_id.startswith("sha256:"):
        raise SystemExit(f"unexpected image digest: {image_id}")

    V1_PATH.parent.mkdir(parents=True, exist_ok=True)
    V2_PATH.parent.mkdir(parents=True, exist_ok=True)
    container_name = f"terraform-baseline-evidence-{uuid.uuid4().hex[:10]}"
    started_at = datetime.now(UTC)
    started = time.perf_counter()
    try:
        subprocess.run(
            [
                "docker",
                "create",
                "--name",
                container_name,
                args.image,
                "benchmark",
                "--repeat",
                "3",
                "--warmup",
                "1",
                "--output",
                "/output/27-kumo-provisioning-v1.json",
            ],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(["docker", "start", "-a", container_name], cwd=ROOT, check=True)
        subprocess.run(
            [
                "docker",
                "cp",
                f"{container_name}:/output/27-kumo-provisioning-v1.json",
                str(V1_PATH),
            ],
            cwd=ROOT,
            check=True,
        )
    finally:
        subprocess.run(
            ["docker", "rm", "-f", container_name], cwd=ROOT, check=False
        )
    duration = time.perf_counter() - started

    result: dict[str, Any] = json.loads(V1_PATH.read_text(encoding="utf-8"))
    apply_samples = [float(sample) for sample in result["samples"]]
    destroy_samples = [float(sample) for sample in result["metrics"]["destroy_seconds"]]
    parity_samples = [float(sample) for sample in result["metrics"]["resource_parity"]]
    config = {
        "adapter": "kumo",
        "resources": 4,
        "warmup": 1,
        "repeat": 3,
        "concurrency": 1,
        "kumo": "0.28.1",
        "terraform": "1.15.8",
        "aws_provider": "5.100.0",
    }
    publication: dict[str, Any] = {
        "schema_version": 2,
        "run_id": str(uuid.uuid4()),
        "project": "terraform-aws-baseline",
        "benchmark_id": "kumo-provisioning",
        "workload": {
            "version": "2.0.0",
            "fixture_digest": combined_digest(SOURCE_PATHS),
            "config_digest": sha256_bytes(
                json.dumps(config, sort_keys=True, separators=(",", ":")).encode()
            ),
            "warmup_iterations": 1,
            "measured_iterations": 3,
            "concurrency": 1,
        },
        "metrics": [
            {
                "name": "kumo_apply_seconds",
                "value": statistics.median(apply_samples),
                "unit": "seconds",
                "direction": "lower_is_better",
                "samples": apply_samples,
                "failures": 0,
                "summary": {
                    "min": min(apply_samples),
                    "median": statistics.median(apply_samples),
                    "max": max(apply_samples),
                },
            },
            {
                "name": "kumo_destroy_seconds",
                "value": statistics.median(destroy_samples),
                "unit": "seconds",
                "direction": "lower_is_better",
                "samples": destroy_samples,
                "failures": 0,
                "summary": {"median": statistics.median(destroy_samples)},
            },
            {
                "name": "resource_parity",
                "value": statistics.mean(parity_samples),
                "unit": "ratio",
                "direction": "target",
                "samples": parity_samples,
                "failures": parity_samples.count(0.0),
                "summary": {"target": 1.0, "resources_per_apply": 4},
            },
        ],
        "execution": {
            "command": "docker run --rm terraform-aws-baseline benchmark --repeat 3",
            "started_at": started_at.isoformat().replace("+00:00", "Z"),
            "duration_seconds": duration,
            "exit_code": 0,
            "repeat": 3,
        },
        "environment": {
            "runtime": f"terraform-1.15.8+kumo-0.28.1+python-{result['environment']['python']}",
            "architecture": result["environment"]["architecture"],
            "hardware_class": (
                "docker-local" if args.producer == "local" else "github-actions-ubuntu"
            ),
        },
        "provenance": {
            "source_commit": source_commit,
            "clean_tree": True,
            "image_ref": f"{args.image}@{image_id}",
            "image_digest": image_id,
            "dependency_lock_digest": combined_digest(LOCK_PATHS),
            "producer": args.producer,
            "artifact_digest": sha256_bytes(V1_PATH.read_bytes()),
        },
        "comparability_key": (
            "kumo-provisioning:2.0.0:resources-4:runs-3:concurrency-1:"
            "terraform-1.15.8:kumo-0.28.1:aws-provider-5.100.0"
        ),
    }
    if args.ci_run_url:
        publication["provenance"]["ci_run_url"] = args.ci_run_url
    V2_PATH.write_text(json.dumps(publication, indent=2) + "\n", encoding="utf-8")
    print(f"v1_result={V1_PATH}")
    print(f"v2_result={V2_PATH}")
    print(f"source_commit={source_commit}")
    print(f"image_digest={image_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
