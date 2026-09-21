# Choose When to Use an RTOS

## What you are doing

Design an RTOS-based alternative, identify synchronization needs, and compare it to the event-loop design. In this version of the exercise you learn by changing and running real C artifacts; there is no reflection or essay to submit.

## Why firmware engineers care

The key ideas are **task, queue, mutex, priority inversion**. Firmware must keep behaving at boundaries and after unusual inputs, not merely in one demonstration. This exercise turns those ideas into behavior the compiler and tests can observe.

## Files you will edit

Edit `task.c` (keep the public declarations in `task.h` unchanged). Do not edit files below `curriculum/` or the hidden acceptance harness. Your personal copy is inside the attempt workspace printed by `./learn status`.

## Required behavior

The architecture battle gates scheduler startup on ready memory and drivers, checks queue burst capacity and execution-plus-blocking deadlines, then decides whether separate RTOS tasks justify their complexity.

## Interface you must preserve

```c
bool startup_services_ready(bool memory_ready, bool drivers_ready, bool scheduler_ready);
bool queue_absorbs_burst(size_t producer_burst, size_t consumer_progress, size_t queue_capacity);
bool periodic_load_fits(uint32_t execution_us, uint32_t blocking_us, uint32_t period_us);
bool rtos_partition_justified(unsigned independent_jobs, bool shared_blocking_io, bool cooperative_deadlines_met);
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
