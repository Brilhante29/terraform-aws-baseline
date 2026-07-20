from __future__ import annotations

import argparse
import json
import platform
import statistics
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/local-baseline.auto.tfvars.json"
DEFAULT_OUTPUT = ROOT / "benchmarks/results/27-local-first.json"


def checked(command: list[str]) -> str:
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def timed(command: list[str]) -> float:
    started = time.perf_counter()
    checked(command)
    return time.perf_counter() - started


def terraform_version() -> str:
    output = checked(["terraform", "version"])
    return output.splitlines()[0].strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark static validation and simulated provisioning.")
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.repeat < 1:
        parser.error("--repeat must be at least 1")

    checked(["terraform", "init", "-backend=false", "-input=false", "-no-color"])
    validation_samples = [
        timed(["terraform", "validate", "-no-color"]) for _ in range(args.repeat)
    ]
    plan_samples: list[float] = []
    with tempfile.TemporaryDirectory(prefix="terraform-aws-baseline-") as temp_dir:
        for index in range(args.repeat):
            plan_path = Path(temp_dir) / f"plan-{index}.tfplan"
            plan_samples.append(
                timed(
                    [
                        "terraform",
                        "plan",
                        "-refresh=false",
                        "-input=false",
                        "-no-color",
                        "-var-file=fixtures/local-baseline.auto.tfvars.json",
                        f"-out={plan_path}",
                    ]
                )
            )

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    display_output = output.relative_to(ROOT).as_posix() if output.is_relative_to(ROOT) else output.as_posix()
    payload = {
        "schema_version": "1.0",
        "fixture_version": "1.0.0",
        "project": "27-terraform-aws-baseline",
        "metric": "provision_time_seconds",
        "value": round(statistics.median(plan_samples), 6),
        "unit": "seconds",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": f"python benchmarks/benchmark.py --repeat {args.repeat} --output {display_output}",
        "repeat": args.repeat,
        "samples": [round(sample, 6) for sample in plan_samples],
        "summary": {
            "validation_median_seconds": round(statistics.median(validation_samples), 6),
            "validation_min_seconds": round(min(validation_samples), 6),
            "plan_median_seconds": round(statistics.median(plan_samples), 6),
            "plan_min_seconds": round(min(plan_samples), 6),
        },
        "environment": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "terraform": terraform_version(),
            "adapter": "terraform_data_local",
            "fixture": "fixtures/local-baseline.auto.tfvars.json",
            "aws_credentials_required": "false",
            "provisioning": "terraform_plan_only",
        },
        "operations": {
            "modules": 3,
            "local_resources": 3,
            "real_cloud_resources": 0,
        },
        "compatibility_diagnostics": {
            "kumo_used": "false",
            "aws_provider_loaded": "false",
            "aws_conformance_claim": "false",
        },
    }
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
