# Budget Firmware Resources

## Your task

Define the interface in `task.c` so this rule holds: Static queue storage is calculated with an overflow check before a RAM budget accepts it. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **RAM, flash, stack, time** into behavior a caller can verify. In firmware, a defect in `queue_storage_size` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `queue_storage_size`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool queue_storage_size(size_t capacity, size_t item_size, size_t *out_bytes);
```

Do not change these declarations.

- `capacity` from `size_t capacity`: number of elements or bytes available; zero is a boundary case.
- `item_size` from `size_t item_size`: an input value; its meaningful range is demonstrated below.
- `out_bytes` from `size_t *out_bytes`: caller-owned destination written only when the operation succeeds.
- `queue_storage_size` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
size_t out=9U; assert(queue_storage_size(8U,12U,&out)&&out==96U); assert(queue_storage_size(0U,12U,&out)&&out==0U); assert(!queue_storage_size(SIZE_MAX,2U,&out)); assert(!queue_storage_size(1U,1U,NULL));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
