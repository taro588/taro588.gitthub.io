"""Run the Toolkit test suite without requiring Maya, 3ds Max, or third-party plugins."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    try:
        import pytest
    except ImportError:
        print("pytest is not installed; use: python -m pip install pytest")
        return 2
    return subprocess.call([sys.executable, "-m", "pytest", "-q"], cwd=ROOT)

if __name__ == "__main__":
    raise SystemExit(main())
