# Implement a Tiny Scheduler

## Your task

Define the interface in `task.c` so this rule holds: One call releases at most one job, advances from the planned deadline to avoid drift, and compares deadlines across wrap. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **period, deadline, wraparound** into behavior a caller can verify. In firmware, a defect in `scheduler_release` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `scheduler_release`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
struct scheduled_task { uint32_t period; uint32_t next_release; unsigned runs; };
bool scheduler_release(struct scheduled_task *task, uint32_t now);
```

Do not change these declarations.

- `task` from `struct scheduled_task *task`: pointer to caller-owned state that the function may update.
- `now` from `uint32_t now`: an input value; its meaningful range is demonstrated below.
- `scheduler_release` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct scheduled_task t={10U,100U,0U}; assert(!scheduler_release(&t,99U)); assert(scheduler_release(&t,100U)&&t.next_release==110U&&t.runs==1U); t.next_release=UINT32_MAX-2U;t.period=5U;assert(scheduler_release(&t,2U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
