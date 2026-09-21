# Build a Library Test Matrix

## Your task

Define the interface in `task.c` so this rule holds: Tests can state and exercise empty, full, wrapped, and invalid ring-buffer invariants independently of implementation. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **unit, consumer, configuration, compatibility** into behavior a caller can verify. In firmware, a defect in `ring_state_valid` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `ring_state_valid`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool ring_state_valid(size_t head, size_t tail, size_t count, size_t capacity);
```

Do not change these declarations.

- `head` from `size_t head`: an input value; its meaningful range is demonstrated below.
- `tail` from `size_t tail`: an input value; its meaningful range is demonstrated below.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `capacity` from `size_t capacity`: number of elements or bytes available; zero is a boundary case.
- `ring_state_valid` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(ring_state_valid(0U,0U,0U,4U)); assert(ring_state_valid(0U,0U,4U,4U)); assert(ring_state_valid(3U,1U,2U,4U)); assert(!ring_state_valid(4U,0U,0U,4U)); assert(!ring_state_valid(0U,0U,1U,0U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
