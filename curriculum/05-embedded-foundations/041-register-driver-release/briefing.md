# Release: Register-Level GPIO Driver

## Your task

Define the interface in `task.c` so this rule holds: The register-driver release validates the pin domain, performs a reserved-bit-preserving field update, and reads the configured field back through a separate query. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **register masks, volatile, API boundary** into behavior a caller can verify. In firmware, a defect in `gpio_pin_valid`, `gpio_mode_set`, `gpio_mode_matches` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `gpio_pin_valid`, `gpio_mode_set`, `gpio_mode_matches`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool gpio_pin_valid(unsigned pin);
bool gpio_mode_set(uint32_t original, unsigned pin, uint32_t mode, uint32_t *out_value);
bool gpio_mode_matches(uint32_t register_value, unsigned pin, uint32_t expected_mode);
```

Do not change these declarations.

- `pin` from `unsigned pin`: an input value; its meaningful range is demonstrated below.
- `gpio_pin_valid` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `original` from `uint32_t original`: an input value; its meaningful range is demonstrated below.
- `pin` from `unsigned pin`: an input value; its meaningful range is demonstrated below.
- `mode` from `uint32_t mode`: an input value; its meaningful range is demonstrated below.
- `out_value` from `uint32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `gpio_mode_set` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `register_value` from `uint32_t register_value`: an input value; its meaningful range is demonstrated below.
- `pin` from `unsigned pin`: an input value; its meaningful range is demonstrated below.
- `expected_mode` from `uint32_t expected_mode`: an input value; its meaningful range is demonstrated below.
- `gpio_mode_matches` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint32_t out=0U;assert(gpio_pin_valid(15U));assert(!gpio_pin_valid(16U));assert(gpio_mode_set(UINT32_MAX,5U,1U,&out));assert(gpio_mode_matches(out,5U,1U));assert((out&~(UINT32_C(3)<<10U))==(UINT32_MAX&~(UINT32_C(3)<<10U)));assert(!gpio_mode_set(0U,16U,1U,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
