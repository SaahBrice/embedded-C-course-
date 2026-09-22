# Inspect a Running Program

## Your task

Define the interface in `task.c` so this rule holds: The debugging release repairs a counted loop, sums and finds the minimum, encodes negative positions in an eight-bit mask, then publishes all results together only after every pointer and extent is valid. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **breakpoints, step, print, backtrace** into behavior a caller can verify. In firmware, a defect in `sample_sum`, `sample_minimum`, `sample_negative_mask`, `sample_window_analyze` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The loop condition uses `i <= count`, so it tries to read one element beyond the live array. Change the bound so only indices strictly smaller than `count` are visited.

## Read the function signature

```c
bool sample_sum(const int16_t *samples, size_t count, int32_t *out_sum);
bool sample_minimum(const int16_t *samples, size_t count, int16_t *out_minimum);
bool sample_negative_mask(const int16_t *samples, size_t count, uint8_t *out_mask);
bool sample_window_analyze(const int16_t *samples, size_t count, int32_t *out_sum, int16_t *out_minimum, uint8_t *out_negative_mask);
```

Do not change these declarations.

- `samples` from `const int16_t *samples`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `out_sum` from `int32_t *out_sum`: caller-owned destination written only when the operation succeeds.
- `sample_sum` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `samples` from `const int16_t *samples`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `out_minimum` from `int16_t *out_minimum`: caller-owned destination written only when the operation succeeds.
- `sample_minimum` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `samples` from `const int16_t *samples`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `out_mask` from `uint8_t *out_mask`: caller-owned destination written only when the operation succeeds.
- `sample_negative_mask` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `samples` from `const int16_t *samples`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `out_sum` from `int32_t *out_sum`: caller-owned destination written only when the operation succeeds.
- `out_minimum` from `int16_t *out_minimum`: caller-owned destination written only when the operation succeeds.
- `out_negative_mask` from `uint8_t *out_negative_mask`: caller-owned destination written only when the operation succeeds.
- `sample_window_analyze` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const int16_t v[]={10,-3,7};int32_t sum=99;int16_t low=99;uint8_t mask=0U;assert(sample_sum(v,3U,&sum)&&sum==14);assert(sample_minimum(v,3U,&low)&&low==-3);assert(sample_negative_mask(v,3U,&mask)&&mask==UINT8_C(0x02));assert(sample_window_analyze(v,3U,&sum,&low,&mask)&&sum==14&&low==-3&&mask==UINT8_C(0x02));assert(!sample_window_analyze(v,0U,&sum,&low,&mask));assert(!sample_window_analyze(v,9U,&sum,&low,&mask));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
