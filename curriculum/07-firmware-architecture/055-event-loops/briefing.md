# Build a Cooperative Event Loop

## Your task

Define the interface in `task.c` so this rule holds: A scheduler can poll this constant-time predicate without blocking; unsigned elapsed time remains valid through counter wrap. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **polling, events, bounded work** into behavior a caller can verify. In firmware, a defect in `task_due` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `task_due`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool task_due(uint32_t now, uint32_t last_run, uint32_t period);
```

Do not change these declarations.

- `now` from `uint32_t now`: an input value; its meaningful range is demonstrated below.
- `last_run` from `uint32_t last_run`: an input value; its meaningful range is demonstrated below.
- `period` from `uint32_t period`: an input value; its meaningful range is demonstrated below.
- `task_due` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(!task_due(14U,10U,5U)); assert(task_due(15U,10U,5U)); assert(task_due(2U,UINT32_MAX-2U,5U)); assert(!task_due(10U,0U,0U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
