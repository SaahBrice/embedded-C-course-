# Final Release: Portable Data Logger

## Your task

Define the interface in `task.c` so this rule holds: The capstone release validates a versioned record shape, hashes exactly the serialized bytes, and accepts a record only when structure and integrity evidence both pass. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **library, host demo, STM32 adapter, documentation, version** into behavior a caller can verify. In firmware, a defect in `logger_record_shape_valid`, `logger_release_checksum`, `logger_release_validate` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `logger_record_shape_valid`, `logger_release_checksum`, `logger_release_validate`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool logger_record_shape_valid(const uint8_t *bytes, size_t length);
uint32_t logger_release_checksum(const uint8_t *bytes, size_t length);
bool logger_release_validate(const uint8_t *bytes, size_t length, uint32_t expected_checksum);
```

Do not change these declarations.

- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `logger_record_shape_valid` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `logger_release_checksum` return type `uint32_t`: returns the result or status defined by the required behavior.
- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `expected_checksum` from `uint32_t expected_checksum`: an input value; its meaningful range is demonstrated below.
- `logger_release_validate` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const uint8_t record[]={1U,1U,42U};assert(logger_record_shape_valid(record,3U));assert(!logger_record_shape_valid(record,2U));assert(logger_release_checksum(record,3U)==UINT32_C(399283687));assert(logger_release_validate(record,3U,UINT32_C(399283687)));assert(!logger_release_validate(record,3U,0U));const uint8_t wrong[]={2U,1U,42U};assert(!logger_record_shape_valid(wrong,3U));assert(logger_release_checksum(NULL,0U)==UINT32_C(2166136261));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
