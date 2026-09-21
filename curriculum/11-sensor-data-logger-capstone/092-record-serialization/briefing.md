# Capstone: Serialize Deterministically

## Your task

Define the interface in `task.c` so this rule holds: `record_serialize` emits an explicit version byte and little-endian fields, independent of structure padding and host byte order. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **wire format, endianness, checksum** into behavior a caller can verify. In firmware, a defect in `record_serialize` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `record_serialize`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
#define RECORD_WIRE_SIZE 9U
struct serial_record { uint32_t timestamp_ms; int32_t value; };
bool record_serialize(const struct serial_record *record, uint8_t *bytes, size_t capacity);
```

Do not change these declarations.

- `record` from `const struct serial_record *record`: read-only input accessed through a pointer; null handling follows the contract.
- `bytes` from `uint8_t *bytes`: pointer to caller-owned state that the function may update.
- `capacity` from `size_t capacity`: number of elements or bytes available; zero is a boundary case.
- `record_serialize` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct serial_record r={UINT32_C(0x12345678),-2}; uint8_t b[RECORD_WIRE_SIZE]={0U}; assert(record_serialize(&r,b,sizeof b)); const uint8_t expected[]={1U,0x78U,0x56U,0x34U,0x12U,0xfeU,0xffU,0xffU,0xffU}; assert(memcmp(b,expected,sizeof b)==0); assert(!record_serialize(&r,b,8U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
