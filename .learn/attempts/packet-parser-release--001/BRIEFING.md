# Release: Binary Packet Parser

## Your task

Define the interface in `task.c` so this rule holds: The parser release validates the whole frame header, decodes little-endian payload bytes without alignment assumptions, and commits a typed packet only after both stages succeed. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **arrays, pointers, structures, bounds checks** into behavior a caller can verify. In firmware, a defect in `packet_header_valid`, `packet_decode_value`, `packet_parse` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `packet_header_valid`, `packet_decode_value`, `packet_parse`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
struct parsed_packet { uint8_t kind; uint16_t value; };
bool packet_header_valid(const uint8_t *bytes, size_t length);
bool packet_decode_value(const uint8_t *bytes, size_t length, uint16_t *out_value);
bool packet_parse(const uint8_t *bytes, size_t length, struct parsed_packet *out_packet);
```

Do not change these declarations.

- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `packet_header_valid` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `out_value` from `uint16_t *out_value`: caller-owned destination written only when the operation succeeds.
- `packet_decode_value` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `out_packet` from `struct parsed_packet *out_packet`: caller-owned destination written only when the operation succeeds.
- `packet_parse` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const uint8_t good[]={1U,2U,0x34U,0x12U};uint16_t value=0U;struct parsed_packet out={9U,9U};assert(packet_header_valid(good,4U));assert(packet_decode_value(good,4U,&value)&&value==UINT16_C(0x1234));assert(packet_parse(good,4U,&out)&&out.kind==1U&&out.value==UINT16_C(0x1234));const uint8_t bad[]={2U,2U,0U,0U};assert(!packet_header_valid(bad,4U));assert(!packet_parse(good,3U,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
