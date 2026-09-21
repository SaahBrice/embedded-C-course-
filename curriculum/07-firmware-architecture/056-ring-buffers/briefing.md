# Implement a Ring Buffer

## Your task

Define the interface in `task.c` so this rule holds: Head owns the next write, tail owns the next read, count distinguishes full from empty, and push rejects new data when full. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **head, tail, full empty policy** into behavior a caller can verify. In firmware, a defect in `byte_ring_push`, `byte_ring_pop` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `byte_ring_push`, `byte_ring_pop`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
#define BYTE_RING_CAPACITY 4U
struct byte_ring { uint8_t data[BYTE_RING_CAPACITY]; size_t head, tail, count; };
bool byte_ring_push(struct byte_ring *ring, uint8_t value);
bool byte_ring_pop(struct byte_ring *ring, uint8_t *out_value);
```

Do not change these declarations.

- `ring` from `struct byte_ring *ring`: pointer to caller-owned state that the function may update.
- `value` from `uint8_t value`: an input value; its meaningful range is demonstrated below.
- `byte_ring_push` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `ring` from `struct byte_ring *ring`: pointer to caller-owned state that the function may update.
- `out_value` from `uint8_t *out_value`: caller-owned destination written only when the operation succeeds.
- `byte_ring_pop` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct byte_ring r={{0U},0U,0U,0U}; uint8_t out=0U; assert(!byte_ring_pop(&r,&out)); for(uint8_t i=1U;i<=4U;++i) assert(byte_ring_push(&r,i)); assert(!byte_ring_push(&r,5U)); assert(byte_ring_pop(&r,&out)&&out==1U); assert(byte_ring_push(&r,5U)); for(uint8_t i=2U;i<=5U;++i) assert(byte_ring_pop(&r,&out)&&out==i);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
