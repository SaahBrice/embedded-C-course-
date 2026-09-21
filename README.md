# Embedded C Career Game

This repository is a guided terminal game for learning C and embedded firmware by writing code. Its 96 coding sublevels are arranged into 11 ordered levels. Every declared topic is reinforced across at least five distinct coding sublevels, and every level ends with an integrative final battle. The campaign begins with one complete tiny C program, then introduces reusable functions before progressing through memory, peripherals, firmware architecture, testing, reusable libraries, advanced embedded work, and a complete sensor data logger.

There are no required reflections or essays. The course uses strict compilation, executable examples, immutable tests, host peripheral simulations, build/install checks, and an explicit STM32 Nucleo-C031C6 hardware checkpoint. Your board appears only where physical hardware adds value; portable code is still developed and tested on the host.

## Start playing

You need Python 3.11 or newer and a C compiler. Make and CMake are used later. From this directory, run:

```bash
./learn doctor
./learn map
./learn start
```

`start` first displays the current level's main objective, learning outcomes, ordered sublevels, and final battle. It then creates or resumes an isolated workspace below `.learn/attempts/`. Each workspace contains a permanent `BRIEFING.md`; read it in your editor, then edit only the learner files in that workspace.

During a sublevel, use:

```bash
./learn status
./learn level
./learn sublevels
./learn lesson
./learn run
./learn test
./learn hint
./learn solution
./learn submit
```

For a function without `main`, `./learn run` supplies a trusted temporary driver. It compiles your actual source, shows real diagnostics, prints each call and its raw return value, then compares the expected and observed condition. `./learn test` runs the complete immutable assessment. `./learn submit` reruns those checks, records a passing sublevel, and unlocks the next one. Only passing the integrative final battle persists a cleared-level record and unlocks the next level.

Hints and worked solutions are unrestricted. Failed checks do not cost lives or points, and tests never edit your source files.

Completed work remains replayable:

```bash
./learn replay first-build
./learn replay-final orientation-toolchain
```

Replay creates a new numbered attempt and preserves earlier work. To remove only one unwanted attempt, use its exact ID: `./learn reset first-build--002 --yes`. Completion history is left unchanged.

## What you will build

The campaign covers compilation, control flow, functions, pointers, memory, modular C, fixed-width arithmetic, registers, `const`, `volatile`, electronics, datasheets, GPIO, interrupts, timers, UART, ADC, PWM, SPI, and I2C. Later levels cover state machines, event loops, callbacks, hardware abstraction, testing, GDB, sanitizers, concurrency, secure parsing, library API design, semantic versioning, packaging, startup and linker concepts, real-time analysis, and RTOS fundamentals.

The final release is an allocation-free sensor data logger with injected hardware ports, deterministic host tests, versioned serialization, persistent buffering, and bounded retry behavior.

Read [Getting Started](docs/GETTING_STARTED.md) for the full play loop, [Curriculum](docs/CURRICULUM.md) for all levels, [STM32 Setup](docs/STM32_SETUP.md) for the board, and [Authoring](docs/AUTHORING.md) to add or insert levels and sublevels.

Maintainers can validate the repository with `./scripts/test_all.sh`. Ordinary course checks never flash hardware. Attempt isolation protects curriculum files, but it is not a security sandbox; run only code you wrote or trust.
