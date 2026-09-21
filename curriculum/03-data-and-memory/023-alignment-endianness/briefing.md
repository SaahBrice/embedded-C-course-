# Decode Portable Byte Layouts

## Your task

Define the interface in `task.c` so this rule holds: Four protocol bytes are decoded in big-endian order without assuming host alignment or byte order. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **padding, alignment, endianness** into behavior a caller can verify. In firmware, a defect in `decode_u32_be` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `decode_u32_be`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool decode_u32_be(const uint8_t *bytes, size_t length, uint32_t *out_value);
```

Do not change these declarations.

- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `out_value` from `uint32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `decode_u32_be` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const uint8_t bytes[]={0x12U,0x34U,0x56U,0x78U}; uint32_t out=0U; assert(decode_u32_be(bytes,4U,&out)&&out==UINT32_C(0x12345678)); assert(!decode_u32_be(bytes,3U,&out)); assert(!decode_u32_be(NULL,4U,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
