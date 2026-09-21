# NUCLEO-C031C6 hardware track

This directory keeps the portable application separate from the STM32CubeC0 adapter. You can develop and test `common/src/app.c` on the host with `make host-test`, then reuse it unchanged in an STM32Cube project.

## Verified board facts

The target is the STM32C031C6 MCU on the MB1717 Nucleo-64 board. The integrated ST-LINK/V2-1 provides debugging/programming and a virtual serial port. In the board's default solder-bridge configuration:

- LD4 USER is active-high on PA5.
- B1 USER is on PC13.
- The ST-LINK virtual COM port uses USART2: PA2 for TX and PA3 for RX.

Sources: ST's [NUCLEO-C031C6 product page](https://www.st.com/en/evaluation-tools/nucleo-c031c6.html), [UM2953 Rev 2 board manual](https://www.st.com/resource/en/user_manual/um2953-stm32c0-nucleo64-board-mb1717-stmicroelectronics.pdf), and [UM2985 STM32CubeC0 guide](https://www.st.com/resource/en/user_manual/um2985-getting-started-with-stm32cubec0-for-stm32c0-series-stmicroelectronics.pdf).

## Setup route

1. Run `./learn doctor` at the repository root.
2. Install STM32CubeIDE or the combination of STM32CubeC0, an Arm GCC toolchain, CMake/Make, and either STM32CubeProgrammer or OpenOCD.
3. In STM32CubeMX/IDE, start from board `NUCLEO-C031C6` and generate a C project.
4. Configure PA5 as an initially-low push-pull output and USART2 asynchronous mode on PA2/PA3. Keep the default ST-LINK VCP solder bridges.
5. Add `common/include/app.h`, `common/src/app.c`, `common/include/board_pins.h`, and `target/board_stm32_hal.c` to the project.
6. After `MX_GPIO_Init()` and `MX_USART2_UART_Init()`, use the integration shown at the bottom of `board_stm32_hal.c`.
7. Build before connecting the board. Connect it through the ST-LINK USB connector, then flash explicitly through the IDE or `./flash.sh --yes path/to/firmware.elf`.

The repository cannot verify electrical behavior without a connected board. `make host-test` verifies the portable contract, including 32-bit timer wrap. `make target-contract-test` also compiles the real Cube adapter against a fake HAL and observes its complete GPIO port/pin, state, UART handle, payload, and timeout calls. The hardware mission still asks you to record the real LD4 and virtual-COM observations.

## Recovery

If flashing fails, disconnect external circuits, reconnect ST-LINK USB, confirm the board appears in the programmer, select “connect under reset,” hold RESET while connecting if necessary, erase only the target MCU through the official programmer, and rebuild the known-good example. Never change jumpers or solder bridges without checking UM2953 and the schematic for your exact board revision.
