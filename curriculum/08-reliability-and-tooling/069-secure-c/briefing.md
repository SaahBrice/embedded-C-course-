# Validate Untrusted Data

## Your task

Define the interface in `task.c` so this rule holds: The received extent is validated before trusting an attacker-controlled payload length or publishing it. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **length trust boundary, integer conversion, fail closed** into behavior a caller can verify. In firmware, a defect in `frame_payload_length` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `frame_payload_length`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool frame_payload_length(const uint8_t *frame, size_t received, size_t *out_length);
```

Do not change these declarations.

- `frame` from `const uint8_t *frame`: read-only input accessed through a pointer; null handling follows the contract.
- `received` from `size_t received`: an input value; its meaningful range is demonstrated below.
- `out_length` from `size_t *out_length`: caller-owned destination written only when the operation succeeds.
- `frame_payload_length` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const uint8_t good[]={1U,2U,0xaaU,0xbbU}; size_t out=0U; assert(frame_payload_length(good,4U,&out)&&out==2U); const uint8_t bad[]={1U,9U}; assert(!frame_payload_length(bad,2U,&out)); assert(!frame_payload_length(good,1U,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
