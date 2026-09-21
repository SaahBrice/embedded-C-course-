# Work Safely with Arrays

## Your task

Define the interface in `task.c` so this rule holds: The first live element seeds both extrema, and every later index is proven smaller than `count`. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **bounds, element count, iteration** into behavior a caller can verify. In firmware, a defect in `sample_minmax` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `sample_minmax`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool sample_minmax(const int16_t *samples, size_t count, int16_t *out_min, int16_t *out_max);
```

Do not change these declarations.

- `samples` from `const int16_t *samples`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `out_min` from `int16_t *out_min`: caller-owned destination written only when the operation succeeds.
- `out_max` from `int16_t *out_max`: caller-owned destination written only when the operation succeeds.
- `sample_minmax` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const int16_t v[] = {7, -2, 19, 4}; int16_t low = 0, high = 0; assert(sample_minmax(v, 4U, &low, &high) && low == -2 && high == 19); assert(sample_minmax(v, 1U, &low, &high) && low == 7 && high == 7); assert(!sample_minmax(v, 0U, &low, &high));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
