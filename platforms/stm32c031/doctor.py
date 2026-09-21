#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from learn_engine.doctor import TOOLS, tool_version


def main() -> int:
    print("NUCLEO-C031C6 tool doctor")
    for _label, tool in TOOLS:
        print(f"{tool}: {tool_version(tool)}")
    print("No build, USB access, or flash operation was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
