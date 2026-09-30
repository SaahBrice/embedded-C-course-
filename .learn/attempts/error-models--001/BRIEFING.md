# Propagate Errors Without Guessing

## Your task

Define the interface in `task.c` so this rule holds: Distinct argument and range statuses propagate meaning; the numeric output is written only on success. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **status codes, out parameters, error context** into behavior a caller can verify. In firmware, a defect in `sensor_scale` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `sensor_scale`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
enum scale_status { SCALE_OK, SCALE_ARGUMENT, SCALE_RANGE };
enum scale_status sensor_scale(uint16_t raw, uint16_t maximum_raw, int32_t *out_milli);
```

Do not change these declarations.

- `raw` from `uint16_t raw`: an input value; its meaningful range is demonstrated below.
- `maximum_raw` from `uint16_t maximum_raw`: an input value; its meaningful range is demonstrated below.
- `out_milli` from `int32_t *out_milli`: caller-owned destination written only when the operation succeeds.
- `sensor_scale` return type `enum scale_status`: returns one of the named status or state values declared above.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
int32_t out = -1; assert(sensor_scale(5U,10U,&out) == SCALE_OK && out == 500); assert(sensor_scale(11U,10U,&out) == SCALE_RANGE); assert(sensor_scale(1U,0U,&out) == SCALE_ARGUMENT);
```

## Expected failure behavior

Return the named failure or safe-state enumerator for rejected work; never invent an out-of-range enum result or partially publish output.
