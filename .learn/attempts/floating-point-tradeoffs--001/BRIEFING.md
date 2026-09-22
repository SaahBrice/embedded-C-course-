# Measure Floating-Point Trade-offs

## Your task

Define the interface in `task.c` so this rule holds: Finite nonnegative volts in the documented range are rounded to integer millivolts; invalid ranges are rejected. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **representation, rounding, fixed point** into behavior a caller can verify. In firmware, a defect in `volts_to_millivolts` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `volts_to_millivolts`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool volts_to_millivolts(double volts, uint32_t *out_millivolts);
```

Do not change these declarations.

- `volts` from `double volts`: an input value; its meaningful range is demonstrated below.
- `out_millivolts` from `uint32_t *out_millivolts`: caller-owned destination written only when the operation succeeds.
- `volts_to_millivolts` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint32_t out=9U; assert(volts_to_millivolts(3.3,&out)&&out==3300U); assert(volts_to_millivolts(0.0006,&out)&&out==1U); assert(!volts_to_millivolts(-0.1,&out)); assert(!volts_to_millivolts(70.0,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
