# Complete Curriculum

The course contains 11 ordered levels and 96 distinct coding sublevels. Most sublevels target 45–60 minutes; release final battles may span several sessions. Each level starts with a readable overview, has at least five progressively unlocked problems, and ends with exactly one final battle.

## Levels

1. **Orientation and Toolchain — 6 sublevels.** Define a first status function, build a complete program, fix strict warnings, connect declarations to build stages, operate on binary/hex values, and finish with a debugger-driven array repair.
2. **C Foundations — 10 sublevels.** Use integer and floating-point representations, expressions, decisions, loops, functions, scope, validated input, and decomposition before releasing a telemetry converter.
3. **Data and Memory — 9 sublevels.** Work safely with arrays, strings, pointers, output parameters, lifetime, structured data, alignment, byte order, and fixed storage before releasing a packet parser.
4. **Professional C — 8 sublevels.** Separate headers and implementations, control macros, design defensive APIs and errors, avoid undefined behavior, preserve portability, and use callbacks before releasing a CRC module.
5. **Embedded Foundations — 8 sublevels.** Connect C to CPU and memory behavior, exact-width values, register masks, qualifiers, memory-mapped I/O, electronics, and datasheets before releasing a GPIO register driver.
6. **Peripheral Engineering — 12 sublevels.** Code GPIO, interrupts, timers, non-blocking time, UART, ADC, PWM, SPI, and I2C against host simulations; inspect the STM32 toolchain and Nucleo-C031C6; then release a peripheral console.
7. **Firmware Architecture — 8 sublevels.** Build state machines, event loops, ring buffers, callbacks, hardware abstraction, configuration, and bounded resource handling before releasing a portable controller.
8. **Reliability and Tooling — 9 sublevels.** Write tests, debug with GDB and sanitizers, act on static analysis, harden arithmetic and concurrency, and parse hostile input before repairing an intermittent reset incident.
9. **Library Forge — 8 sublevels.** Design and document APIs, hide internals, apply semantic versioning, configure and test a library, install it with Make/CMake, and prove a relocated consumer can use it.
10. **Advanced Embedded Development — 7 sublevels.** Trace startup, linker scripts, and memory sections; design safe boot; schedule bounded work; calculate deadlines; and finish by choosing when an RTOS is justified.
11. **Sensor Data-Logger Capstone — 11 sublevels.** Turn requirements into injected interfaces, validate and timestamp samples, buffer and serialize records, handle storage and transport failures, integrate the product, and publish the final portable release.

Run `./learn level` to read the active level's full objective and outcomes. Run `./learn sublevels <level-id>` to list its titles, IDs, and final battle.

## Supporting artifacts

`platforms/host` provides deterministic C simulations for GPIO, UART, timers, ADC, memory-mapped registers, interrupts, PWM, SPI, and I2C. `platforms/stm32c031` contains portable board code, host contract tests, NUCLEO-C031C6 pin mappings, a CubeC0 adapter, a Cortex-M0+ target project, tool diagnostics, and a guarded flash command.

`library/record_queue` is the completed Library Forge reference with Make and CMake packaging. `capstone/reference` is the finished data-logger product with a runnable demonstration and failure-injection tests.

Stable sublevel IDs and versions preserve completion history. Authors can add intermediary sublevels by assigning a new order and updating prerequisites, or add whole levels through the declarative level catalog.
