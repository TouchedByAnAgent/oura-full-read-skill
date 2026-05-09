#!/usr/bin/env python3
"""Run the bundled oura-full-read CLI from this skill."""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


def main() -> None:
    skill_root = Path(__file__).resolve().parents[1]
    src_path = skill_root / "assets" / "oura-full-read" / "src"
    if not src_path.exists():
        raise SystemExit(f"bundled source not found: {src_path}")
    sys.path.insert(0, str(src_path))
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    runpy.run_module("oura_full_read.cli", run_name="__main__")


if __name__ == "__main__":
    main()
