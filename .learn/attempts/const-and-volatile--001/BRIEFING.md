# Apply const and volatile Correctly

## Your task

Define the interface in `task.c` so this rule holds: The pointer prevents writes through this view while volatile preserves the observable register read. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **read-only interfaces, observable side effects, optimization** into behavior a caller can verify. In firmware, a defect in `sample_volatile_register` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `sample_volatile_register`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool sample_volatile_register(volatile const uint32_t *reg, uint32_t *out_value);
```

Do not change these declarations.

- `reg` from `volatile const uint32_t *reg`: read-only input accessed through a pointer; null handling follows the contract.
- `out_value` from `uint32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `sample_volatile_register` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
volatile uint32_t reg=UINT32_C(0xa5); uint32_t out=0U; assert(sample_volatile_register(&reg,&out)&&out==UINT32_C(0xa5)); reg=7U; assert(sample_volatile_register(&reg,&out)&&out==7U); assert(!sample_volatile_register(NULL,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
