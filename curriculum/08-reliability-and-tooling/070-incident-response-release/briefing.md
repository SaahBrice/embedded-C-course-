# Incident: Intermittent Logger Reset

## Your task

Define the interface in `task.c` so this rule holds: The incident-response release reproduces wraparound timeout behavior, checks a persisted ring invariant, and makes one explicit recovery decision from independent fault evidence. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **reproduction, fault isolation, regression test** into behavior a caller can verify. In firmware, a defect in `watchdog_elapsed`, `ring_indices_valid`, `recovery_required` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `watchdog_elapsed`, `ring_indices_valid`, `recovery_required`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool watchdog_elapsed(uint32_t now, uint32_t last_kick, uint32_t timeout);
bool ring_indices_valid(size_t head, size_t tail, size_t count, size_t capacity);
bool recovery_required(bool watchdog_expired, bool ring_valid, unsigned consecutive_errors, unsigned error_limit);
```

Do not change these declarations.

- `now` from `uint32_t now`: an input value; its meaningful range is demonstrated below.
- `last_kick` from `uint32_t last_kick`: an input value; its meaningful range is demonstrated below.
- `timeout` from `uint32_t timeout`: an input value; its meaningful range is demonstrated below.
- `watchdog_elapsed` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `head` from `size_t head`: an input value; its meaningful range is demonstrated below.
- `tail` from `size_t tail`: an input value; its meaningful range is demonstrated below.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `capacity` from `size_t capacity`: number of elements or bytes available; zero is a boundary case.
- `ring_indices_valid` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `watchdog_expired` from `bool watchdog_expired`: a true/false input flag.
- `ring_valid` from `bool ring_valid`: a true/false input flag.
- `consecutive_errors` from `unsigned consecutive_errors`: an input value; its meaningful range is demonstrated below.
- `error_limit` from `unsigned error_limit`: an input value; its meaningful range is demonstrated below.
- `recovery_required` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(!watchdog_elapsed(109U,100U,10U));assert(watchdog_elapsed(110U,100U,10U));assert(watchdog_elapsed(3U,UINT32_MAX-5U,8U));assert(ring_indices_valid(3U,1U,2U,4U));assert(!ring_indices_valid(4U,0U,0U,4U));assert(!recovery_required(false,true,2U,3U));assert(recovery_required(true,true,0U,3U));assert(recovery_required(false,false,0U,3U));assert(recovery_required(false,true,3U,3U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
