# Replace Blocking Delays

## Your task

Define the interface in `task.c` so this rule holds: Each call performs bounded work, toggles only after one complete period, and remains correct when the tick counter wraps. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **deadlines, wrap-safe subtraction, cooperation** into behavior a caller can verify. In firmware, a defect in `blinker_update` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `blinker_update`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
struct blinker { uint32_t last_change; uint32_t period; bool level; };
bool blinker_update(struct blinker *blinker, uint32_t now);
```

Do not change these declarations.

- `blinker` from `struct blinker *blinker`: pointer to caller-owned state that the function may update.
- `now` from `uint32_t now`: an input value; its meaningful range is demonstrated below.
- `blinker_update` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct blinker b = {10U,5U,false}; assert(!blinker_update(&b,14U) && !b.level); assert(blinker_update(&b,15U) && b.level && b.last_change == 15U); b.last_change=UINT32_MAX-2U; b.period=5U; assert(blinker_update(&b,2U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
