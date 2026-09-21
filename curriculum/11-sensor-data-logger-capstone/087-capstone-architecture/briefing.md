# Capstone: Partition the System

## Your task

Define the interface in `task.c` so this rule holds: Initialization succeeds only when all four injected hardware boundaries are present. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **portable core, ports, adapters** into behavior a caller can verify. In firmware, a defect in `logger_ports_ready` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `logger_ports_ready`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool logger_ports_ready(bool sensor, bool clock, bool storage, bool transport);
```

Do not change these declarations.

- `sensor` from `bool sensor`: a true/false input flag.
- `clock` from `bool clock`: a true/false input flag.
- `storage` from `bool storage`: a true/false input flag.
- `transport` from `bool transport`: a true/false input flag.
- `logger_ports_ready` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(logger_ports_ready(true,true,true,true)); assert(!logger_ports_ready(false,true,true,true)); assert(!logger_ports_ready(true,false,true,true)); assert(!logger_ports_ready(true,true,false,true)); assert(!logger_ports_ready(true,true,true,false));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
