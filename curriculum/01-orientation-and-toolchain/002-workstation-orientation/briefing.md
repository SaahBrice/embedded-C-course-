# Implement Your First Firmware Function

## Your task

This sublevel teaches the simplest firmware-style status contract. `boot_count` is an unsigned count of successful boots already observed. An unsigned value cannot be negative. The `U` suffix in `0U`, `1U`, and `42U` tells C that each literal is unsigned.

You are **not** writing a complete program and must **not** create `main`. The trusted test and visible-run harnesses provide `main` for you. Your entire coding job is to define the function already declared in `task.h`.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. `./learn run` compiles your function with the visible driver and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

A firmware module often reports readiness with a small status function that another module calls during boot. If zero and nonzero counts are confused, later initialization may run before the system has ever booted successfully. This small contract teaches declaration versus definition, unsigned input, and status returns before adding a complete program.

`task.c` contains only a comment, so `firmware_status` has been declared but not defined. Add its definition there. The function currently cannot be linked or called at all.

## Read the function signature

```c
int firmware_status(unsigned boot_count);
```

Do not change this declaration.

- `boot_count` is the number of successful boots already observed. Because it is `unsigned`, its range starts at zero; it can never represent a negative count.
- The `int` return value is a status code: `0` means ready, while `-1` means no successful boot has occurred.

## Concrete examples

- `firmware_status(0U)` must return `-1`: zero means the firmware has not recorded a successful boot.
- `firmware_status(1U)` must return `0`: one successful boot is enough.
- `firmware_status(42U)` must return `0`: every positive boot count represents success.

The return value is a status, not the number of boots. Here, zero means success and `-1` means the required boot has not happened.

## Expected failure behavior

There is no invalid value in the `unsigned` input range. Reporting not-ready is an ordinary status result, not a crash or compile failure, and the function must have no side effects.
