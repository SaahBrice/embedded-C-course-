# Design Defensive APIs

## Your task

Define the interface in `task.c` so this rule holds: Null pointers are legal only for a zero-length operation, capacity is checked before the first write, and failure leaves storage untouched. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **preconditions, postconditions, invalid arguments** into behavior a caller can verify. In firmware, a defect in `bounded_copy` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `bounded_copy`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool bounded_copy(uint8_t *destination, size_t capacity, const uint8_t *source, size_t count);
```

Do not change these declarations.

- `destination` from `uint8_t *destination`: pointer to caller-owned state that the function may update.
- `capacity` from `size_t capacity`: number of elements or bytes available; zero is a boundary case.
- `source` from `const uint8_t *source`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `bounded_copy` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint8_t d[4] = {0U}; const uint8_t s[] = {1U,2U,3U}; assert(bounded_copy(d,4U,s,3U) && d[2] == 3U); assert(!bounded_copy(d,2U,s,3U)); assert(bounded_copy(NULL,0U,NULL,0U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
