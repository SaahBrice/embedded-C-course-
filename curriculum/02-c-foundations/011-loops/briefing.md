# Process a Sample Window

## Your task

Define the interface in `task.c` so this rule holds: The loop invariant is that `total` contains exactly the first `i` samples; an empty window has no average. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **for, while, loop invariants** into behavior a caller can verify. In firmware, a defect in `sample_average` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `sample_average`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool sample_average(const int16_t *samples, size_t count, int32_t *out_average);
```

Do not change these declarations.

- `samples` from `const int16_t *samples`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `out_average` from `int32_t *out_average`: caller-owned destination written only when the operation succeeds.
- `sample_average` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const int16_t v[] = {3, 6, 9, 12}; int32_t avg = 0; assert(sample_average(v, 4U, &avg) && avg == 7); assert(!sample_average(v, 0U, &avg)); assert(!sample_average(NULL, 1U, &avg));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
