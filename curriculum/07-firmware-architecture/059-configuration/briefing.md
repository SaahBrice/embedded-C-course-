# Make Configuration Explicit

## Your task

Define the interface in `task.c` so this rule holds: Runtime configuration accepts a bounded nonzero period and an ordered inclusive measurement interval. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **compile-time, run-time, validation** into behavior a caller can verify. In firmware, a defect in `controller_config_valid` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `controller_config_valid`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool controller_config_valid(uint32_t sample_period_ms, int32_t low_limit, int32_t high_limit);
```

Do not change these declarations.

- `sample_period_ms` from `uint32_t sample_period_ms`: an input value; its meaningful range is demonstrated below.
- `low_limit` from `int32_t low_limit`: an input value; its meaningful range is demonstrated below.
- `high_limit` from `int32_t high_limit`: an input value; its meaningful range is demonstrated below.
- `controller_config_valid` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(controller_config_valid(1000U,-40,125)); assert(!controller_config_valid(0U,-40,125)); assert(!controller_config_valid(60001U,-40,125)); assert(!controller_config_valid(10U,5,4));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
