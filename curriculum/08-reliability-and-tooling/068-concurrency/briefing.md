# Reason About Shared State

## Your task

Define the interface in `task.c` so this rule holds: Single-word sequence snapshots are ordered with defined unsigned wraparound and an explicit half-range rule. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **atomicity, race, critical section** into behavior a caller can verify. In firmware, a defect in `sequence_is_newer` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `sequence_is_newer`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool sequence_is_newer(uint32_t candidate, uint32_t current);
```

Do not change these declarations.

- `candidate` from `uint32_t candidate`: an input value; its meaningful range is demonstrated below.
- `current` from `uint32_t current`: an input value; its meaningful range is demonstrated below.
- `sequence_is_newer` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(sequence_is_newer(11U,10U)); assert(!sequence_is_newer(10U,10U)); assert(sequence_is_newer(0U,UINT32_MAX)); assert(!sequence_is_newer(UINT32_C(0x80000000),0U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
