# Analyze Real-Time Schedulability

## Your task

Define the interface in `task.c` so this rule holds: Worst-case execution plus blocking must fit the period, using subtraction to avoid overflow. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **worst-case execution, period, utilization, latency** into behavior a caller can verify. In firmware, a defect in `nonpreemptive_deadline_met` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `nonpreemptive_deadline_met`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool nonpreemptive_deadline_met(uint32_t wcet_us, uint32_t blocking_us, uint32_t period_us);
```

Do not change these declarations.

- `wcet_us` from `uint32_t wcet_us`: an input value; its meaningful range is demonstrated below.
- `blocking_us` from `uint32_t blocking_us`: an input value; its meaningful range is demonstrated below.
- `period_us` from `uint32_t period_us`: an input value; its meaningful range is demonstrated below.
- `nonpreemptive_deadline_met` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(nonpreemptive_deadline_met(200U,100U,1000U)); assert(nonpreemptive_deadline_met(500U,500U,1000U)); assert(!nonpreemptive_deadline_met(900U,200U,1000U)); assert(!nonpreemptive_deadline_met(1001U,0U,1000U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
