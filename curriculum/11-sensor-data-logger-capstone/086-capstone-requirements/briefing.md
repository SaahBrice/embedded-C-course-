# Capstone: Define the Product

## Your task

Define the interface in `task.c` so this rule holds: Logger requirements enforce a nonzero period, at most ten-percent jitter, and a bounded static record capacity. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **requirements, acceptance criteria, constraints** into behavior a caller can verify. In firmware, a defect in `logger_requirements_valid` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `logger_requirements_valid`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool logger_requirements_valid(uint32_t period_ms, uint32_t jitter_ms, size_t record_capacity);
```

Do not change these declarations.

- `period_ms` from `uint32_t period_ms`: an input value; its meaningful range is demonstrated below.
- `jitter_ms` from `uint32_t jitter_ms`: an input value; its meaningful range is demonstrated below.
- `record_capacity` from `size_t record_capacity`: an input value; its meaningful range is demonstrated below.
- `logger_requirements_valid` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(logger_requirements_valid(1000U,100U,64U)); assert(!logger_requirements_valid(0U,0U,64U)); assert(!logger_requirements_valid(1000U,101U,64U)); assert(!logger_requirements_valid(1000U,50U,1U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
