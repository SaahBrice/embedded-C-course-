# Level 6: Peripheral Engineering

## Main objective

Control and integrate GPIO, time, interrupts, serial buses, analog conversion, and the STM32 board boundary.

## What you should know before starting

Complete Level 5; this level builds directly on its C contracts and debugging habits.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Release: Peripheral Console**.

## What you will build and learn

- Drive GPIO, time, interrupts, UART, ADC, PWM, SPI, and I2C through deterministic simulations
- Keep blocking, ownership, range, and timeout behavior explicit at peripheral boundaries
- Build and observe the STM32 path before releasing a peripheral console

## Ordered sublevels

1. **Drive Digital I/O** (`gpio`) — Implement `gpio_output_level`: Logical device state is converted to an electrical output level in one place, including active-low wiring.
2. **Keep Interrupt Work Bounded** (`interrupts`) — Implement `interrupt_capture`, `interrupt_take`: The interrupt callback performs one bounded mailbox write, never overwrites a pending event, and foreground code explicitly consumes ownership.
3. **Schedule with Hardware Timers** (`timers`) — Implement `deadline_reached`: Signed interpretation of unsigned subtraction gives a wrap-safe deadline decision when intervals remain below half the counter range.
4. **Replace Blocking Delays** (`nonblocking-time`) — Implement `blinker_update`: Each call performs bounded work, toggles only after one complete period, and remains correct when the tick counter wraps.
5. **Build a UART Boundary** (`uart`) — Implement `uart_line_feed`: `uart_line_feed` accepts one byte per call, always preserves termination, reports a complete line at newline, and rejects overflow.
6. **Acquire Analog Samples** (`adc`) — Implement `adc_code_to_mv`: Resolution determines the maximum code; widened arithmetic and half-up rounding map only valid codes into millivolts.
7. **Control Output with PWM** (`pwm`) — Implement `pwm_compare`: Widening prevents multiplication overflow, 0 and 100 percent map to the endpoints, and invalid percentages are rejected.
8. **Transact over SPI** (`spi`) — Implement `spi_build_read`: The portable transaction builder sets the protocol read bit and dummy byte only after validating address and capacity.
9. **Transact over I2C** (`i2c`) — Implement `i2c_address_byte`: A seven-bit device address and the transfer direction remain separate until the bus address byte is formed.
10. **Prepare the STM32 Toolchain** (`stm32-toolchain-checkpoint`) — Implement `elf_header_targets_arm`: The compiled artifact is accepted only when its ELF magic and machine field identify a little-endian ARM target.
11. **Bring Up the Nucleo-C031C6** (`stm32-board-checkpoint`) — Build the ARM target and record only the NUCLEO-C031C6 flash, LED, and UART evidence you observe.
12. **Release: Peripheral Console** (`peripheral-console-release`) — FINAL BATTLE — Implement `console_parse`, `console_is_led_command`, `console_led_level`: The peripheral-console release parses complete UART text into typed commands, classifies actuator work, and converts a logical LED request to the configured electrical level.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **digital events, timing, and serial I/O** is practised in: Drive Digital I/O, Keep Interrupt Work Bounded, Schedule with Hardware Timers, Replace Blocking Delays, Build a UART Boundary, Transact over SPI, Transact over I2C, Release: Peripheral Console
- **range-checked peripheral conversion** is practised in: Schedule with Hardware Timers, Replace Blocking Delays, Acquire Analog Samples, Control Output with PWM, Transact over SPI, Transact over I2C, Release: Peripheral Console
- **simulation through target integration** is practised in: Drive Digital I/O, Build a UART Boundary, Acquire Analog Samples, Transact over SPI, Transact over I2C, Prepare the STM32 Toolchain, Bring Up the Nucleo-C031C6, Release: Peripheral Console

## Final battle

**Release: Peripheral Console** is the last required sublevel. It integrates **Drive Digital I/O**, **Build a UART Boundary**, **Bring Up the Nucleo-C031C6**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
