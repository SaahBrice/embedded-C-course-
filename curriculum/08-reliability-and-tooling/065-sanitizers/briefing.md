# Use Host Sanitizers

## Your task

Define the interface in `task.c` so this rule holds: The sanitizer-backed build verifies that byte count derives from a validated element count and no zero-length call dereferences null. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **AddressSanitizer, UndefinedBehaviorSanitizer, reproduction** into behavior a caller can verify. In firmware, a defect in `copy_samples` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The loop uses `index <= count`, which reads `values[count]` one element past the array. Sanitizers expose that access; repair the loop bound and preserve the null rules.

## Read the function signature

```c
bool copy_samples(int16_t *destination, size_t capacity, const int16_t *source, size_t count);
```

Do not change these declarations.

- `destination` from `int16_t *destination`: pointer to caller-owned state that the function may update.
- `capacity` from `size_t capacity`: number of elements or bytes available; zero is a boundary case.
- `source` from `const int16_t *source`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `copy_samples` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
int16_t d[3]={0}; const int16_t s[]={1,2,3,4}; assert(copy_samples(d,3U,s,3U)&&d[2]==3); assert(!copy_samples(d,3U,s,4U)); assert(copy_samples(NULL,0U,NULL,0U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
