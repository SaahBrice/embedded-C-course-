# Read Pointer Relationships

## Your task

Define the interface in `task.c` so this rule holds: A pointer and element count share one provenance-safe contract: null is accepted only for zero elements, impossible byte extents are rejected, and iteration never compares unrelated pointers. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **address, dereference, pointer arithmetic** into behavior a caller can verify. In firmware, a defect in `checked_sum` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `checked_sum`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool checked_sum(const int32_t *values, size_t count, int64_t *out_sum);
```

Do not change these declarations.

- `values` from `const int32_t *values`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `out_sum` from `int64_t *out_sum`: caller-owned destination written only when the operation succeeds.
- `checked_sum` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const int32_t v[] = {4, 5, 6}; int64_t sum = -1; assert(checked_sum(v, 3U, &sum) && sum == 15); assert(checked_sum(NULL, 0U, &sum) && sum == 0); assert(!checked_sum(NULL, 1U, &sum)); assert(!checked_sum(v, SIZE_MAX, &sum)); assert(!checked_sum(v, 3U, NULL));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
