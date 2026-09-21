# Release: Portable Sensor Controller

## Your task

Define the interface in `task.c` so this rule holds: The controller release combines wrap-safe scheduling, bounded sample acceptance, and an explicit state update that counts only ready measurements at a due release. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **state machine, event loop, HAL, ring buffer** into behavior a caller can verify. In firmware, a defect in `sensor_controller_due`, `sensor_sample_acceptable`, `sensor_controller_update` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `sensor_controller_due`, `sensor_sample_acceptable`, `sensor_controller_update`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
struct sensor_controller { uint32_t period; uint32_t last_sample; unsigned samples; };
bool sensor_controller_due(const struct sensor_controller *controller, uint32_t now);
bool sensor_sample_acceptable(bool sensor_ready, int32_t value, int32_t minimum, int32_t maximum);
bool sensor_controller_update(struct sensor_controller *controller, uint32_t now, bool sensor_ready);
```

Do not change these declarations.

- `controller` from `const struct sensor_controller *controller`: read-only input accessed through a pointer; null handling follows the contract.
- `now` from `uint32_t now`: an input value; its meaningful range is demonstrated below.
- `sensor_controller_due` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `sensor_ready` from `bool sensor_ready`: a true/false input flag.
- `value` from `int32_t value`: an input value; its meaningful range is demonstrated below.
- `minimum` from `int32_t minimum`: an input value; its meaningful range is demonstrated below.
- `maximum` from `int32_t maximum`: an input value; its meaningful range is demonstrated below.
- `sensor_sample_acceptable` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `controller` from `struct sensor_controller *controller`: pointer to caller-owned state that the function may update.
- `now` from `uint32_t now`: an input value; its meaningful range is demonstrated below.
- `sensor_ready` from `bool sensor_ready`: a true/false input flag.
- `sensor_controller_update` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct sensor_controller c={10U,100U,0U};assert(!sensor_controller_due(&c,109U));assert(sensor_controller_due(&c,110U));assert(sensor_sample_acceptable(true,25,-40,125));assert(!sensor_sample_acceptable(false,25,-40,125));assert(!sensor_sample_acceptable(true,126,-40,125));assert(sensor_controller_update(&c,110U,true)&&c.samples==1U&&c.last_sample==110U);assert(!sensor_controller_update(&c,120U,false));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
