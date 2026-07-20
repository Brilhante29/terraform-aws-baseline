from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "README.md",
    "project.yaml",
    "REFERENCES.md",
    "AGENTS.md",
    "Dockerfile",
    "sdd/spec.md",
    "sdd/benchmark-plan.md",
    "sdd/architecture-decision.md",
    "sdd/technical-decision.md",
    "sdd/agent-handoff.md",
    "sdd/reuse-improvement-review.md",
    "openspec/artifacts/verification.md",
    "fixtures/local-baseline.auto.tfvars.json",
    "benchmarks/results/27-local-first.json",
)


def run(command: list[str]) -> None:
    print("$ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def validate_benchmark() -> None:
    path = ROOT / "benchmarks/results/27-local-first.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    required = {"project", "metric", "value", "unit", "timestamp", "command"}
    missing = required - payload.keys()
    if missing:
        raise ValueError(f"benchmark is missing fields: {sorted(missing)}")
    if payload["project"] != "27-terraform-aws-baseline":
        raise ValueError("benchmark project does not match project.yaml")
    if payload["metric"] != "provision_time_seconds":
        raise ValueError("benchmark metric does not match the project contract")
    if not isinstance(payload["value"], (int, float)) or payload["value"] < 0:
        raise ValueError("benchmark value must be a non-negative number")


def validate_text_contracts() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if not readme.startswith("#27 "):
        raise ValueError("README must start with #27")
    if "provision_time_seconds" not in readme:
        raise ValueError("README must report the primary benchmark")
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            raise FileNotFoundError(relative)
    for relative in ("sdd/spec.md", "sdd/architecture-decision.md", "sdd/technical-decision.md"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        if "<pending>" in text or "<project-name>" in text or "<style>" in text:
            raise ValueError(f"unresolved placeholder in {relative}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-terraform", action="store_true")
    args = parser.parse_args()

    try:
        validate_text_contracts()
        validate_benchmark()
        run([sys.executable, "-m", "compileall", "-q", "tools", "tests", "benchmarks"])
        run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
        if not args.skip_terraform:
            run(["terraform", "fmt", "-check", "-recursive"])
            run(["terraform", "init", "-backend=false", "-input=false", "-no-color"])
            run(["terraform", "validate", "-no-color"])
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print("strict project validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
