from __future__ import annotations

import subprocess
import sys


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if command == "validate":
        args = [sys.executable, "tools/validate.py"]
    elif command == "benchmark":
        args = [sys.executable, "benchmarks/benchmark.py", *sys.argv[2:]]
    else:
        print(f"unsupported command: {command}", file=sys.stderr)
        return 2
    return subprocess.run(args, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
