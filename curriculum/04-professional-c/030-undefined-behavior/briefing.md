# Recognize Undefined Behavior

## Your task

Define the interface in `task.c` so this rule holds: The shift count is narrower than the type width and the value is proven representable before the shift expression executes. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **overflow, invalid shifts, aliasing, sequence rules** into behavior a caller can verify. In firmware, a defect in `safe_left_shift` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The starter dereferences `out_value` and shifts immediately. A null output pointer, shift of 32 or more, or unrepresentable result reaches undefined or unwanted behavior before any validation.

## Read the function signature

```c
bool safe_left_shift(uint32_t value, unsigned shift, uint32_t *out_value);
```

Do not change these declarations.

- `value` from `uint32_t value`: an input value; its meaningful range is demonstrated below.
- `shift` from `unsigned shift`: an input value; its meaningful range is demonstrated below.
- `out_value` from `uint32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `safe_left_shift` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint32_t out = 0U; assert(safe_left_shift(3U,4U,&out) && out == 48U); assert(!safe_left_shift(1U,32U,&out)); assert(!safe_left_shift(UINT32_MAX,1U,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
