#!/usr/bin/env bash
set -u

if [[ $# -ne 2 || "$1" != "--yes" ]]; then
    echo "Usage: ./flash.sh --yes <firmware.elf>" >&2
    echo "Flashing is explicit and requires --yes." >&2
    exit 2
fi

firmware=$2
if [[ ! -f "$firmware" ]]; then
    echo "Firmware does not exist: $firmware" >&2
    exit 2
fi

if command -v STM32_Programmer_CLI >/dev/null 2>&1; then
    exec STM32_Programmer_CLI -c port=SWD -w "$firmware" -v -rst
fi
if command -v openocd >/dev/null 2>&1; then
    case "$firmware" in
        *[!A-Za-z0-9_./+-]*)
            echo "Firmware path cannot be represented safely in an OpenOCD command: $firmware" >&2
            exit 2
            ;;
    esac
    exec openocd -f interface/stlink.cfg -f target/stm32c0x.cfg -c "program $firmware verify reset exit"
fi

echo "Neither STM32_Programmer_CLI nor OpenOCD is installed." >&2
exit 2
