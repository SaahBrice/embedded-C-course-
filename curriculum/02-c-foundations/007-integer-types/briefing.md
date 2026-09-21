# Choose Integer Types Deliberately

## Your task

Define the interface in `task.c` so this rule holds: The range check proves whether a signed 32-bit measurement can be represented by int16_t before narrowing. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **signedness, range, integer promotion** into behavior a caller can verify. In firmware, a defect in `temperature_fits_i16` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `temperature_fits_i16`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool temperature_fits_i16(int32_t milli_celsius);
```

Do not change these declarations.

- `milli_celsius` from `int32_t milli_celsius`: an input value; its meaningful range is demonstrated below.
- `temperature_fits_i16` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(temperature_fits_i16(INT16_MIN)); assert(temperature_fits_i16(INT16_MAX)); assert(!temperature_fits_i16((int32_t)INT16_MIN-1)); assert(!temperature_fits_i16((int32_t)INT16_MAX+1));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
