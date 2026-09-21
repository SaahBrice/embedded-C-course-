# Design a Safe Boot Flow

## Your task

Define the interface in `task.c` so this rule holds: Successful boot advances one ordered phase; any failure or invalid continuation returns outputs to the safe phase. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **reset cause, initialization order, safe state** into behavior a caller can verify. In firmware, a defect in `boot_next` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `boot_next`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
enum boot_phase { BOOT_SAFE_OUTPUTS, BOOT_CLOCKS, BOOT_DRIVERS, BOOT_ENABLE_ACTUATORS, BOOT_READY };
enum boot_phase boot_next(enum boot_phase current, bool step_ok);
```

Do not change these declarations.

- `current` from `enum boot_phase current`: an input value; its meaningful range is demonstrated below.
- `step_ok` from `bool step_ok`: a true/false input flag.
- `boot_next` return type `enum boot_phase`: returns one of the named status or state values declared above.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(boot_next(BOOT_SAFE_OUTPUTS,true)==BOOT_CLOCKS); assert(boot_next(BOOT_DRIVERS,true)==BOOT_ENABLE_ACTUATORS); assert(boot_next(BOOT_CLOCKS,false)==BOOT_SAFE_OUTPUTS); assert(boot_next(BOOT_READY,true)==BOOT_SAFE_OUTPUTS);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
