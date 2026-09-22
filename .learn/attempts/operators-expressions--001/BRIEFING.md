# Control Expression Evaluation

## Your task

Define the interface in `task.c` so this rule holds: The expression sets requested bits, clears requested bits last, and contains no hidden side effects. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **precedence, short circuiting, side effects** into behavior a caller can verify. In firmware, a defect in `status_bits_update` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `status_bits_update`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
uint32_t status_bits_update(uint32_t status, uint32_t set_mask, uint32_t clear_mask);
```

Do not change these declarations.

- `status` from `uint32_t status`: an input value; its meaningful range is demonstrated below.
- `set_mask` from `uint32_t set_mask`: an input value; its meaningful range is demonstrated below.
- `clear_mask` from `uint32_t clear_mask`: an input value; its meaningful range is demonstrated below.
- `status_bits_update` return type `uint32_t`: returns the result or status defined by the required behavior.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(status_bits_update(UINT32_C(0x0a), UINT32_C(0x05), UINT32_C(0x08)) == UINT32_C(0x07)); assert(status_bits_update(UINT32_MAX, 0U, UINT32_MAX) == 0U);
```

## Expected failure behavior

Produce exactly the documented value for every accepted input. Any rejected operation must use its documented status without undefined behavior or a partial state update.
