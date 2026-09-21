# Read a Peripheral Datasheet

## Your task

Define the interface in `task.c` so this rule holds: A value is proven to fit a datasheet field before shifting and masking it into register position. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **register map, reset value, field access** into behavior a caller can verify. In firmware, a defect in `datasheet_field_encode` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `datasheet_field_encode`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool datasheet_field_encode(uint32_t value, unsigned shift, uint32_t mask, uint32_t *out_bits);
```

Do not change these declarations.

- `value` from `uint32_t value`: an input value; its meaningful range is demonstrated below.
- `shift` from `unsigned shift`: an input value; its meaningful range is demonstrated below.
- `mask` from `uint32_t mask`: an input value; its meaningful range is demonstrated below.
- `out_bits` from `uint32_t *out_bits`: caller-owned destination written only when the operation succeeds.
- `datasheet_field_encode` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint32_t out=0U; assert(datasheet_field_encode(2U,4U,UINT32_C(0x30),&out)&&out==UINT32_C(0x20)); assert(!datasheet_field_encode(4U,4U,UINT32_C(0x30),&out)); assert(!datasheet_field_encode(1U,32U,UINT32_MAX,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
