# Schedule with Hardware Timers

## Your task

Define the interface in `task.c` so this rule holds: Signed interpretation of unsigned subtraction gives a wrap-safe deadline decision when intervals remain below half the counter range. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **tick, compare, overflow** into behavior a caller can verify. In firmware, a defect in `deadline_reached` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `deadline_reached`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool deadline_reached(uint32_t now, uint32_t deadline);
```

Do not change these declarations.

- `now` from `uint32_t now`: an input value; its meaningful range is demonstrated below.
- `deadline` from `uint32_t deadline`: an input value; its meaningful range is demonstrated below.
- `deadline_reached` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(deadline_reached(100U,100U)); assert(deadline_reached(101U,100U)); assert(!deadline_reached(99U,100U)); assert(deadline_reached(2U,UINT32_MAX-2U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
