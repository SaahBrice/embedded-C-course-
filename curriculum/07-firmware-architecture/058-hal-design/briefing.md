# Define a Hardware Abstraction Boundary

## Your task

Define the interface in `task.c` so this rule holds: Portable policy depends only on injected operations and context; sensor failure drives the output to its documented safe alarm state. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **ports, adapters, portable core** into behavior a caller can verify. In firmware, a defect in `bool`, `void`, `controller_step` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `bool`, `void`, `controller_step`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
struct controller_hal { void *context; bool (*read_sensor)(void *, int32_t *); void (*set_alarm)(void *, bool); };
bool controller_step(const struct controller_hal *hal, int32_t maximum);
```

Do not change these declarations.

- `hal` from `const struct controller_hal *hal`: read-only input accessed through a pointer; null handling follows the contract.
- `maximum` from `int32_t maximum`: an input value; its meaningful range is demonstrated below.
- `controller_step` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct fake_hal fake={42,false,true}; struct controller_hal hal={&fake,fake_read,fake_alarm}; assert(controller_step(&hal,40)&&fake.alarm); fake.value=10; assert(controller_step(&hal,40)&&!fake.alarm); fake.read_ok=false; assert(!controller_step(&hal,40)&&fake.alarm);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
