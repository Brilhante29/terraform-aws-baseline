from __future__ import annotations

import subprocess
import sys


def run(arguments: list[str]) -> int:
    return subprocess.run(arguments, check=False).returncode


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "verify"
    rest = sys.argv[2:]
    if command == "validate":
        return run([sys.executable, "tools/validate.py"])
    if command == "benchmark":
        return run([sys.executable, "benchmarks/benchmark.py", *rest])
    if command == "validate-publication":
        return run([sys.executable, "tools/validate-publication.py"])
    if command == "verify":
        validation = run([sys.executable, "tools/validate.py"])
        if validation != 0:
            return validation
        return run(
            [
                sys.executable,
                "benchmarks/benchmark.py",
                "--repeat",
                "3",
                "--output",
                "/output/27-kumo-provisioning-v1.json",
            ]
        )
    print(f"unsupported command: {command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
