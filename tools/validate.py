from __future__ import annotations

import json
import re
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
    "adapters/kumo/main.tf",
    "adapters/kumo/provider.tf",
    "adapters/aws/main.tf",
    "modules/application-baseline/main.tf",
    "fixtures/kumo-baseline.tfvars.json",
    "sdd/spec.md",
    "sdd/benchmark-plan.md",
    "sdd/architecture-decision.md",
    "sdd/technical-decision.md",
    "sdd/agent-handoff.md",
    "sdd/reuse-improvement-review.md",
    "openspec/artifacts/verification.md",
)


def run(command: list[str]) -> None:
    print("$ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def text_contract_errors() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if not readme.startswith("# Terraform AWS Baseline\n"):
        errors.append("README must start with # Terraform AWS Baseline")
    if "kumo_apply_seconds" not in readme:
        errors.append("README must report kumo_apply_seconds")
    project = (ROOT / "project.yaml").read_text(encoding="utf-8")
    if re.search(r"(?m)^status:\s*(benchmarked|published)\s*$", project) is None:
        errors.append("project status must be benchmarked or published")
    for relative in (
        "sdd/spec.md",
        "sdd/architecture-decision.md",
        "sdd/technical-decision.md",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        if any(marker in text for marker in ("<pending>", "<project-name>", "<style>")):
            errors.append(f"unresolved placeholder in {relative}")
    return errors


def fixture_errors() -> list[str]:
    fixture = json.loads(
        (ROOT / "fixtures/kumo-baseline.tfvars.json").read_text(encoding="utf-8")
    )
    errors: list[str] = []
    if fixture.get("baseline_name") != "fixture-baseline":
        errors.append("fixture baseline_name changed")
    serialized = json.dumps(fixture).lower()
    for forbidden in ("access_key", "secret_key", "password", "token"):
        if forbidden in serialized:
            errors.append(f"fixture contains forbidden secret-shaped key: {forbidden}")
    return errors


def main() -> int:
    errors = text_contract_errors() + fixture_errors()
    for error in errors:
        print(f"validation error: {error}", file=sys.stderr)
    if errors:
        return 1
    commands = [
        [sys.executable, "-m", "compileall", "-q", "tools", "tests", "benchmarks"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        ["terraform", "fmt", "-check", "-recursive"],
        [
            "terraform",
            "-chdir=adapters/kumo",
            "init",
            "-backend=false",
            "-input=false",
            "-no-color",
        ],
        ["terraform", "-chdir=adapters/kumo", "validate", "-no-color"],
        [
            "terraform",
            "-chdir=adapters/aws",
            "init",
            "-backend=false",
            "-input=false",
            "-no-color",
        ],
        ["terraform", "-chdir=adapters/aws", "validate", "-no-color"],
    ]
    if (ROOT / ".git").exists():
        commands.append([sys.executable, "tools/validate-publication.py"])
    else:
        print("publication provenance deferred: full Git checkout is not mounted")
    failures: list[str] = []
    for command in commands:
        try:
            run(command)
        except (FileNotFoundError, subprocess.CalledProcessError) as error:
            failures.append(f"{' '.join(command)}: {error}")
    for failure in failures:
        print(f"validation error: {failure}", file=sys.stderr)
    if failures:
        return 1
    print("strict project validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
