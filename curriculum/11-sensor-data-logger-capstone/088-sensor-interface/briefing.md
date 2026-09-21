# Capstone: Sensor Port

## Your task

Define the interface in `task.c` so this rule holds: The sensor port preserves unavailable and range failures as different statuses and commits only a validated reading. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **sample type, status, fake sensor** into behavior a caller can verify. In firmware, a defect in `sensor_status`, `sensor_read_checked` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `sensor_status`, `sensor_read_checked`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
enum sensor_status { SENSOR_OK, SENSOR_UNAVAILABLE, SENSOR_RANGE };
typedef enum sensor_status (*sensor_read_fn)(void *context, int32_t *out_value);
enum sensor_status sensor_read_checked(sensor_read_fn read, void *context, int32_t minimum, int32_t maximum, int32_t *out_value);
```

Do not change these declarations.

- `context` from `*sensor_read_fn)(void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `out_value` from `int32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `sensor_status` return type `typedef enum`: returns one of the named status or state values declared above.
- `read` from `sensor_read_fn read`: an input value; its meaningful range is demonstrated below.
- `context` from `void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `minimum` from `int32_t minimum`: an input value; its meaningful range is demonstrated below.
- `maximum` from `int32_t maximum`: an input value; its meaningful range is demonstrated below.
- `out_value` from `int32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `sensor_read_checked` return type `enum sensor_status`: returns one of the named status or state values declared above.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct fake_sensor f={SENSOR_OK,25}; int32_t out=0; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_OK&&out==25); f.value=101; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_RANGE); f.status=SENSOR_UNAVAILABLE; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_UNAVAILABLE);
```

## Expected failure behavior

Return the named failure or safe-state enumerator for rejected work; never invent an out-of-range enum result or partially publish output.
