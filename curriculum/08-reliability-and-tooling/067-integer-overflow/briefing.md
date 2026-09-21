# Harden Arithmetic

## Your task

Define the interface in `task.c` so this rule holds: `checked_scale` performs multiplication in a wider defined type and narrows only after both signed limits are proven. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **checked operations, saturation, conversion** into behavior a caller can verify. In firmware, a defect in `checked_scale` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `checked_scale`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool checked_scale(int32_t value, int32_t multiplier, int32_t *out_value);
```

Do not change these declarations.

- `value` from `int32_t value`: an input value; its meaningful range is demonstrated below.
- `multiplier` from `int32_t multiplier`: an input value; its meaningful range is demonstrated below.
- `out_value` from `int32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `checked_scale` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
int32_t out=0; assert(checked_scale(1000,2000,&out)&&out==2000000); assert(checked_scale(-7,6,&out)&&out==-42); assert(!checked_scale(INT32_MAX,2,&out)); assert(!checked_scale(INT32_MIN,-1,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
