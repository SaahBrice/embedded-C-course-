# Release: Telemetry Converter

## Your task

Define the interface in `task.c` so this rule holds: The telemetry release validates the physical range, performs deterministic milli-degree conversion, and refuses to publish a measurement when the sensor reports a fault. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **control flow, functions, validation, formatting** into behavior a caller can verify. In firmware, a defect in `celsius_in_sensor_range`, `celsius_to_milli`, `telemetry_prepare` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `celsius_in_sensor_range`, `celsius_to_milli`, `telemetry_prepare`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool celsius_in_sensor_range(double celsius);
bool celsius_to_milli(double celsius, int32_t *out_milli_celsius);
bool telemetry_prepare(double celsius, bool sensor_fault, int32_t *out_milli_celsius);
```

Do not change these declarations.

- `celsius` from `double celsius`: an input value; its meaningful range is demonstrated below.
- `celsius_in_sensor_range` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `celsius` from `double celsius`: an input value; its meaningful range is demonstrated below.
- `out_milli_celsius` from `int32_t *out_milli_celsius`: caller-owned destination written only when the operation succeeds.
- `celsius_to_milli` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `celsius` from `double celsius`: an input value; its meaningful range is demonstrated below.
- `sensor_fault` from `bool sensor_fault`: a true/false input flag.
- `out_milli_celsius` from `int32_t *out_milli_celsius`: caller-owned destination written only when the operation succeeds.
- `telemetry_prepare` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
int32_t v=77;assert(celsius_in_sensor_range(-40.0));assert(!celsius_in_sensor_range(125.1));assert(celsius_to_milli(21.125,&v)&&v==21125);assert(celsius_to_milli(-0.0006,&v)&&v==-1);v=77;assert(telemetry_prepare(3.3,false,&v)&&v==3300);assert(!telemetry_prepare(3.3,true,&v)&&v==3300);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
