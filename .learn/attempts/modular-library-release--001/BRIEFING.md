# Release: Portable CRC Module

## Your task

Define the interface in `task.c` so this rule holds: The library release exposes a one-byte primitive, a counted-buffer operation, and a verification API through one self-contained header and separately compiled implementation. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **public API, private state, tests, consumer build** into behavior a caller can verify. In firmware, a defect in `crc8_update`, `crc8`, `crc8_verify` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `crc8_update`, `crc8`, `crc8_verify`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
uint8_t crc8_update(uint8_t crc, uint8_t byte);
uint8_t crc8(const uint8_t *bytes, size_t length);
bool crc8_verify(const uint8_t *bytes, size_t length, uint8_t expected);
```

Do not change these declarations.

- `crc` from `uint8_t crc`: an input value; its meaningful range is demonstrated below.
- `byte` from `uint8_t byte`: an input value; its meaningful range is demonstrated below.
- `crc8_update` return type `uint8_t`: returns the result or status defined by the required behavior.
- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `crc8` return type `uint8_t`: returns the result or status defined by the required behavior.
- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `expected` from `uint8_t expected`: an input value; its meaningful range is demonstrated below.
- `crc8_verify` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const uint8_t data[]={1U,2U,3U};assert(crc8_update(0U,1U)==UINT8_C(0x07));assert(crc8(data,3U)==UINT8_C(0x48));assert(crc8(NULL,0U)==0U);assert(crc8_verify(data,3U,UINT8_C(0x48)));assert(!crc8_verify(data,3U,UINT8_C(0x49)));assert(!crc8_verify(NULL,1U,0U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
