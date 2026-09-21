# Use Fixed-Width Integers

## Your task

Define the interface in `task.c` so this rule holds: The counter has an exact 32-bit representation and saturates instead of wrapping at its maximum wire value. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **stdint, UINT32_C, format macros** into behavior a caller can verify. In firmware, a defect in `saturating_counter_add` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `saturating_counter_add`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
uint32_t saturating_counter_add(uint32_t counter, uint32_t increment);
```

Do not change these declarations.

- `counter` from `uint32_t counter`: an input value; its meaningful range is demonstrated below.
- `increment` from `uint32_t increment`: an input value; its meaningful range is demonstrated below.
- `saturating_counter_add` return type `uint32_t`: returns the result or status defined by the required behavior.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(saturating_counter_add(10U,20U) == 30U); assert(saturating_counter_add(UINT32_MAX-1U,2U) == UINT32_MAX); assert(saturating_counter_add(UINT32_MAX,0U) == UINT32_MAX);
```

## Expected failure behavior

Produce exactly the documented value for every accepted input. Any rejected operation must use its documented status without undefined behavior or a partial state update.
