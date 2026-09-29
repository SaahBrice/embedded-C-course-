# Model a Sensor Packet

## Your task

Define the interface in `task.c` so this rule holds: The enum is the union tag: code reads only the member selected by a recognized tag and rejects every unknown value. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **structures, unions, enumerations** into behavior a caller can verify. In firmware, a defect in `packet_value` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `packet_value`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
enum packet_kind { PACKET_TEMPERATURE, PACKET_HUMIDITY };
struct sensor_packet { enum packet_kind kind; union { int16_t temperature_centi_c; uint16_t humidity_centi_percent; } payload; };
bool packet_value(const struct sensor_packet *packet, int32_t *out_value);
```

Do not change these declarations.

- `packet` from `const struct sensor_packet *packet`: read-only input accessed through a pointer; null handling follows the contract.
- `out_value` from `int32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `packet_value` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct sensor_packet t = {PACKET_TEMPERATURE, {.temperature_centi_c = -125}}; int32_t value = 0;
assert(packet_value(&t, &value) && value == -125); struct sensor_packet h = {PACKET_HUMIDITY, {.humidity_centi_percent = 4567U}}; assert(packet_value(&h, &value) && value == 4567); t.kind = (enum packet_kind)99; assert(!packet_value(&t, &value));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
