# Manipulate Register Bits

## Your task

Define the interface in `task.c` so this rule holds: The field value is validated against the shifted mask before a clear-and-set update preserves all unrelated bits. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **mask, shift, set clear toggle** into behavior a caller can verify. In firmware, a defect in `register_field_write` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `register_field_write`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool register_field_write(uint32_t original, uint32_t mask, unsigned shift, uint32_t field_value, uint32_t *out_value);
```

Do not change these declarations.

- `original` from `uint32_t original`: an input value; its meaningful range is demonstrated below.
- `mask` from `uint32_t mask`: an input value; its meaningful range is demonstrated below.
- `shift` from `unsigned shift`: an input value; its meaningful range is demonstrated below.
- `field_value` from `uint32_t field_value`: an input value; its meaningful range is demonstrated below.
- `out_value` from `uint32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `register_field_write` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint32_t out = 0U; assert(register_field_write(UINT32_C(0xa5a5000f),UINT32_C(0x70),4U,5U,&out)); assert(out == UINT32_C(0xa5a5005f)); assert(!register_field_write(0U,UINT32_C(0x70),4U,8U,&out)); assert(!register_field_write(0U,0U,0U,0U,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
