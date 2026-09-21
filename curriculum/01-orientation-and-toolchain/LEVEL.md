# Level 1: Orientation and Toolchain

## Main objective

Learn how a C source file becomes a running program and use compiler and debugger evidence to repair it.

## What you should know before starting

No C knowledge is assumed. You only need a terminal and text editor.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Inspect a Running Program**.

## What you will build and learn

- Compile and run a complete C program with exact output and exit status
- Read strict compiler diagnostics and repair type, range, and conversion defects
- Use binary, hexadecimal, build-stage, and debugger evidence to locate a defect

## Ordered sublevels

1. **Build Your First C Program** (`first-build`) — Edit the supplied `main` so the program prints exactly `firmware ready` with a newline and exits successfully.
2. **Implement Your First Firmware Function** (`workstation-orientation`) — Define `firmware_status` in `task.c`; the supplied driver checks zero, one, and larger unsigned boot counts.
3. **Treat Warnings as Defects** (`compiler-warnings`) — Implement `adc_to_millivolts`: The multiplication is widened before it occurs, range errors are reported, and strict warnings remain enabled.
4. **Trace Source to Executable** (`source-to-program`) — Implement `linked_increment`: A separately declared function produces input plus one, rejects overflow, and writes output only on success.
5. **Decode Binary and Hexadecimal** (`binary-and-hex`) — Implement `swap_nibbles`: The high and low four-bit nibbles exchange positions without changing any bit.
6. **Inspect a Running Program** (`gdb-first-steps`) — FINAL BATTLE — Implement `sample_sum`, `sample_minimum`, `sample_negative_mask`, `sample_window_analyze`: The debugging release repairs a counted loop, sums and finds the minimum, encodes negative positions in an eight-bit mask, then publishes all results together only after every pointer and extent is valid.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **strict diagnostics as defects** is practised in: Build Your First C Program, Implement Your First Firmware Function, Treat Warnings as Defects, Trace Source to Executable, Decode Binary and Hexadecimal, Inspect a Running Program
- **source, translation, and linking** is practised in: Build Your First C Program, Implement Your First Firmware Function, Treat Warnings as Defects, Trace Source to Executable, Inspect a Running Program
- **representation and debugging evidence** is practised in: Implement Your First Firmware Function, Treat Warnings as Defects, Trace Source to Executable, Decode Binary and Hexadecimal, Inspect a Running Program

## Final battle

**Inspect a Running Program** is the last required sublevel. It integrates **Treat Warnings as Defects**, **Trace Source to Executable**, **Decode Binary and Hexadecimal**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
