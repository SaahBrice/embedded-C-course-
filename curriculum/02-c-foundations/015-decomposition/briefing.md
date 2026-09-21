# Decompose a Firmware Ticket

## Your task

Define the interface in `task.c` so this rule holds: Parse-free transformation is decomposed into offset, widened scaling, range validation, and one final output commit. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **contracts, cohesion, coupling** into behavior a caller can verify. In firmware, a defect in `scale_offset_sample` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `scale_offset_sample`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool scale_offset_sample(int32_t raw, int32_t offset, int32_t scale, int32_t *out_value);
```

Do not change these declarations.

- `raw` from `int32_t raw`: an input value; its meaningful range is demonstrated below.
- `offset` from `int32_t offset`: an input value; its meaningful range is demonstrated below.
- `scale` from `int32_t scale`: an input value; its meaningful range is demonstrated below.
- `out_value` from `int32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `scale_offset_sample` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
int32_t out=0; assert(scale_offset_sample(10,-2,3,&out)&&out==24); assert(scale_offset_sample(-5,5,9,&out)&&out==0); assert(!scale_offset_sample(INT32_MAX,1,1,&out)); assert(!scale_offset_sample(1,1,1,NULL));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
