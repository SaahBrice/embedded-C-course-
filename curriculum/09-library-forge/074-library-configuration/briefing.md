# Configure Without Forking

## Your task

Define the interface in `task.c` so this rule holds: Queue configuration accepts only supported power-of-two capacities while treating policy as an explicit option. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **configuration struct, feature macro, defaults** into behavior a caller can verify. In firmware, a defect in `queue_config_valid` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `queue_config_valid`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool queue_config_valid(size_t capacity, bool overwrite_oldest);
```

Do not change these declarations.

- `capacity` from `size_t capacity`: number of elements or bytes available; zero is a boundary case.
- `overwrite_oldest` from `bool overwrite_oldest`: a true/false input flag.
- `queue_config_valid` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(queue_config_valid(2U,false)); assert(queue_config_valid(128U,true)); assert(!queue_config_valid(0U,false)); assert(!queue_config_valid(3U,false)); assert(!queue_config_valid(2048U,true));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
