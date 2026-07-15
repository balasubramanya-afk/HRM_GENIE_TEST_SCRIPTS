#!/usr/bin/env python3
from pathlib import Path
import runpy


if __name__ == "__main__":
    script_path = Path(__file__).resolve().parent / "tests" / "automation.py"
    runpy.run_path(str(script_path), run_name="__main__")
