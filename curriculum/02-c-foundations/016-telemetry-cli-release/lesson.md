# Release: Telemetry Converter

## What you are doing

Build a complete host telemetry converter from a written interface and black-box acceptance checks. In this version of the exercise you learn by changing and running real C artifacts; there is no reflection or essay to submit.

## Why firmware engineers care

The key ideas are **control flow, functions, validation, formatting**. Firmware must keep behaving at boundaries and after unusual inputs, not merely in one demonstration. This exercise turns those ideas into behavior the compiler and tests can observe.

## Files you will edit

Edit `task.c` (keep the public declarations in `task.h` unchanged). Do not edit files below `curriculum/` or the hidden acceptance harness. Your personal copy is inside the attempt workspace printed by `./learn status`.

## Required behavior

The telemetry release validates the physical range, performs deterministic milli-degree conversion, and refuses to publish a measurement when the sensor reports a fault.

## Interface you must preserve

```c
bool celsius_in_sensor_range(double celsius);
bool celsius_to_milli(double celsius, int32_t *out_milli_celsius);
bool telemetry_prepare(double celsius, bool sensor_fault, int32_t *out_milli_celsius);
```

## A practical way to begin

1. Read the complete starter and public interface before changing it.
2. Find the placeholder or deliberate defect and predict the first failing case.
3. Make the smallest correct change while keeping strict compiler warnings enabled.
4. Run `./learn test` and address the first useful diagnostic.
5. Check the zero/empty case, an ordinary case, and the first invalid or maximum case.

## Common mistake

Do not weaken the function signature, compiler flags, error result, or bounds just to make one example work. A passing implementation must preserve the contract for callers that you cannot see.

## Success looks like

Implement the declared C interface so every normal, boundary, and invalid case in the immutable harness passes. Run `./learn test`; every required check must report `PASS`. Use `./learn solution` whenever you need the worked implementation—solutions carry no penalty.
