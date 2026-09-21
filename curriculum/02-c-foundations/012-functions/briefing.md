# Extract Testable Functions

## Your task

Define the interface in `task.c` so this rule holds: `clamp_i32` is a pure, independently testable calculation with explicit behavior for an invalid interval. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **parameters, return values, single responsibility** into behavior a caller can verify. In firmware, a defect in `clamp_i32` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `clamp_i32`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
int32_t clamp_i32(int32_t value, int32_t minimum, int32_t maximum);
```

Do not change these declarations.

- `value` from `int32_t value`: an input value; its meaningful range is demonstrated below.
- `minimum` from `int32_t minimum`: an input value; its meaningful range is demonstrated below.
- `maximum` from `int32_t maximum`: an input value; its meaningful range is demonstrated below.
- `clamp_i32` return type `int32_t`: returns the result or status defined by the required behavior.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(clamp_i32(5, 0, 10) == 5); assert(clamp_i32(-1, 0, 10) == 0); assert(clamp_i32(11, 0, 10) == 10); assert(clamp_i32(4, 7, 3) == 7);
```

## Expected failure behavior

Produce exactly the documented value for every accepted input. Any rejected operation must use its documented status without undefined behavior or a partial state update.
