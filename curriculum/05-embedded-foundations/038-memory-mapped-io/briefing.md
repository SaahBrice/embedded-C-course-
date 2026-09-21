# Model Memory-Mapped I/O

## Your task

Define the interface in `task.c` so this rule holds: The volatile register is read once and written once; the pure mask calculation between those observable accesses is explicit. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **volatile access, register offsets, read-modify-write** into behavior a caller can verify. In firmware, a defect in `register_update` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `register_update`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool register_update(volatile uint32_t *reg, uint32_t clear_mask, uint32_t set_mask);
```

Do not change these declarations.

- `reg` from `volatile uint32_t *reg`: pointer to caller-owned state that the function may update.
- `clear_mask` from `uint32_t clear_mask`: an input value; its meaningful range is demonstrated below.
- `set_mask` from `uint32_t set_mask`: an input value; its meaningful range is demonstrated below.
- `register_update` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
volatile uint32_t reg = UINT32_C(0xf0); assert(register_update(&reg,UINT32_C(0x30),UINT32_C(0x05)) && reg == UINT32_C(0xc5)); assert(!register_update(NULL,0U,0U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
