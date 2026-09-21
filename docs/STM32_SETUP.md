# STM32 Nucleo-C031C6 Setup

The early campaign and all portable firmware logic run without a board. Physical checkpoints use your NUCLEO-C031C6 only after you understand C, bits, registers, qualifiers, and peripheral concepts in simulation.

Run `./learn doctor` first. The host path needs Python, a C compiler, and Make. The target-build path additionally needs `arm-none-eabi-gcc` and STM32CubeC0. Run `./scripts/setup_arm_toolchain.sh` once to install both in your user-owned data directory without `sudo`; it does not alter USB permissions or flash hardware. An ARM-aware GDB, OpenOCD, or STM32CubeProgrammer is useful later for physical debugging and flashing.

The board is an MB1717 Nucleo-64 carrying an STM32C031C6 and integrated ST-LINK/V2-1. According to ST's UM2953 Rev 2, LD4 USER is active-high on PA5, B1 USER is on PC13, and the default virtual COM port is USART2 on PA2/PA3 through SB27/SB32. The course constants preserve all four port/pin pairs, and the target-adapter contract test executes the PA5 output plus the USART2 handle and payload boundary against a fake HAL.

The repository already owns the application, startup integration, interrupt file, runtime support, linker script, GPIO/UART initialization, and build recipe in `platforms/stm32c031/target_project`. The setup script fetches the official STM32CubeC0 v1.4.1 checkout and the build refuses any commit other than the one pinned in that project's README.

First run `make -C platforms/stm32c031 host-test target-contract-test target-build`. The final target prints FLASH/RAM use, creates `target_project/build/nucleo-c031c6.elf`, and verifies that its ELF machine is ARM. Connect the ST-LINK USB port only when that build is clean. Flash from CubeIDE, or explicitly invoke `platforms/stm32c031/flash.sh --yes path/to/firmware.elf`. The script rejects non-ELF input and refuses to run without `--yes`; no ordinary game test invokes it.

Expected observations are an initial UART message on the ST-LINK virtual serial port and an LD4 toggle every 500 milliseconds. Record the actual serial device, output, and LED behavior in the hardware mission. Physical success cannot be honestly automated by a host-only test.

If bring-up fails, distinguish build, probe, permission, flash, and application failures. Check the cable supports data, confirm ST-LINK enumerates, verify the selected board and target, inspect the first programmer error, and try a reset. Do not change solder bridges from their default state without consulting the schematic.

Authoritative references are ST's [NUCLEO-C031C6 product page](https://www.st.com/en/evaluation-tools/nucleo-c031c6.html), [UM2953 board manual](https://www.st.com/resource/en/user_manual/um2953-stm32c0-nucleo64-board-mb1717-stmicroelectronics.pdf), and [UM2985 STM32CubeC0 guide](https://www.st.com/resource/en/user_manual/um2985-getting-started-with-stm32cubec0-for-stm32c0-series-stmicroelectronics.pdf).
