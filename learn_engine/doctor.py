from __future__ import annotations

import shutil
import subprocess


TOOLS = (
    ("Python", "python3"),
    ("Host C compiler", "cc"),
    ("Make", "make"),
    ("CMake", "cmake"),
    ("GDB", "gdb"),
    ("ARM GCC", "arm-none-eabi-gcc"),
    ("ARM GDB", "arm-none-eabi-gdb"),
    ("OpenOCD", "openocd"),
    ("STM32CubeProgrammer", "STM32_Programmer_CLI"),
)


def tool_version(executable: str) -> str:
    path = shutil.which(executable)
    if path is None:
        return "not found"
    try:
        completed = subprocess.run(
            [path, "--version"], capture_output=True, text=True, timeout=3, check=False
        )
        first = (completed.stdout or completed.stderr).splitlines()
        return first[0] if first else path
    except (OSError, subprocess.TimeoutExpired):
        return path
