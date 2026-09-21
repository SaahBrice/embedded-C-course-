# Connect Firmware to Electronics

## Your task

Define the interface in `task.c` so this rule holds: The logical LED request is converted to the correct electrical output level for active-high or active-low wiring. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **voltage, current, pull resistors, active levels** into behavior a caller can verify. In firmware, a defect in `led_output_level` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `led_output_level`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool led_output_level(bool active_low, bool led_on);
```

Do not change these declarations.

- `active_low` from `bool active_low`: a true/false input flag.
- `led_on` from `bool led_on`: a true/false input flag.
- `led_output_level` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(led_output_level(false,true)); assert(!led_output_level(false,false)); assert(!led_output_level(true,true)); assert(led_output_level(true,false));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
