# Route Fault States

## Your task

Define the interface in `task.c` so this rule holds: Fault status has priority; otherwise the inclusive sensor range is accepted and out-of-range data is retried. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **if, switch, enumerated states** into behavior a caller can verify. In firmware, a defect in `classify_measurement` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `classify_measurement`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
enum measurement_action { ACTION_ACCEPT, ACTION_RETRY, ACTION_SHUTDOWN };
enum measurement_action classify_measurement(int32_t value, bool sensor_fault);
```

Do not change these declarations.

- `value` from `int32_t value`: an input value; its meaningful range is demonstrated below.
- `sensor_fault` from `bool sensor_fault`: a true/false input flag.
- `classify_measurement` return type `enum measurement_action`: returns one of the named status or state values declared above.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(classify_measurement(20000, false) == ACTION_ACCEPT); assert(classify_measurement(-40001, false) == ACTION_RETRY); assert(classify_measurement(125001, false) == ACTION_RETRY); assert(classify_measurement(20000, true) == ACTION_SHUTDOWN);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
