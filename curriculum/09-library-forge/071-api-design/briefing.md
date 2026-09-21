# Design a Stable Library API

## Your task

Define the interface in `task.c` so this rule holds: The public operation exposes a narrow status-returning contract and never publishes a value beyond its configured limit. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **consumer needs, opaque types, error contract** into behavior a caller can verify. In firmware, a defect in `counter_add_bounded` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `counter_add_bounded`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool counter_add_bounded(unsigned current, unsigned increment, unsigned limit, unsigned *out_value);
```

Do not change these declarations.

- `current` from `unsigned current`: an input value; its meaningful range is demonstrated below.
- `increment` from `unsigned increment`: an input value; its meaningful range is demonstrated below.
- `limit` from `unsigned limit`: an input value; its meaningful range is demonstrated below.
- `out_value` from `unsigned *out_value`: caller-owned destination written only when the operation succeeds.
- `counter_add_bounded` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
unsigned out=0U; assert(counter_add_bounded(3U,4U,10U,&out)&&out==7U); assert(counter_add_bounded(10U,0U,10U,&out)&&out==10U); assert(!counter_add_bounded(9U,2U,10U,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
