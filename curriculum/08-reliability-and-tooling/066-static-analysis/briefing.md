# Act on Static Analysis

## Your task

Define the interface in `task.c` so this rule holds: Null and bounds findings are repaired with executable checks before the array access occurs. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **data flow, false positive, warning policy** into behavior a caller can verify. In firmware, a defect in `checked_array_read` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `checked_array_read`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool checked_array_read(const int32_t *values, size_t count, size_t index, int32_t *out_value);
```

Do not change these declarations.

- `values` from `const int32_t *values`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `index` from `size_t index`: an input value; its meaningful range is demonstrated below.
- `out_value` from `int32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `checked_array_read` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const int32_t values[]={4,8,15}; int32_t out=0; assert(checked_array_read(values,3U,2U,&out)&&out==15); assert(!checked_array_read(values,3U,3U,&out)); assert(!checked_array_read(NULL,3U,0U,&out));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
