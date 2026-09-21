# Release: Portable Sensor Controller

## What you are doing

Integrate the architecture modules into a deterministic, host-tested sensor controller. In this version of the exercise you learn by changing and running real C artifacts; there is no reflection or essay to submit.

## Why firmware engineers care

The key ideas are **state machine, event loop, HAL, ring buffer**. Firmware must keep behaving at boundaries and after unusual inputs, not merely in one demonstration. This exercise turns those ideas into behavior the compiler and tests can observe.

## Files you will edit

Edit `task.c` (keep the public declarations in `task.h` unchanged). Do not edit files below `curriculum/` or the hidden acceptance harness. Your personal copy is inside the attempt workspace printed by `./learn status`.

## Required behavior

The controller release combines wrap-safe scheduling, bounded sample acceptance, and an explicit state update that counts only ready measurements at a due release.

## Interface you must preserve

```c
struct sensor_controller { uint32_t period; uint32_t last_sample; unsigned samples; };
bool sensor_controller_due(const struct sensor_controller *controller, uint32_t now);
bool sensor_sample_acceptable(bool sensor_ready, int32_t value, int32_t minimum, int32_t maximum);
bool sensor_controller_update(struct sensor_controller *controller, uint32_t now, bool sensor_ready);
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
