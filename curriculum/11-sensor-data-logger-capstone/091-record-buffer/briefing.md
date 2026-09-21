# Capstone: Buffer Records

## Your task

Define the interface in `task.c` so this rule holds: The fixed-capacity ring rejects new records when full and retains FIFO ownership across physical wraparound. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **fixed capacity, full policy, ordering** into behavior a caller can verify. In firmware, a defect in `record_ring_push`, `record_ring_pop` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `record_ring_push`, `record_ring_pop`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
#define RECORD_RING_CAPACITY 3U
struct log_record { uint32_t timestamp; int32_t value; };
struct record_ring { struct log_record data[RECORD_RING_CAPACITY]; size_t head,tail,count; };
bool record_ring_push(struct record_ring *ring, struct log_record record);
bool record_ring_pop(struct record_ring *ring, struct log_record *out_record);
```

Do not change these declarations.

- `ring` from `struct record_ring *ring`: pointer to caller-owned state that the function may update.
- `record` from `struct log_record record`: an input value; its meaningful range is demonstrated below.
- `record_ring_push` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `ring` from `struct record_ring *ring`: pointer to caller-owned state that the function may update.
- `out_record` from `struct log_record *out_record`: caller-owned destination written only when the operation succeeds.
- `record_ring_pop` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct record_ring q={{{0U,0}},0U,0U,0U}; struct log_record out={0U,0}; for(int32_t i=1;i<=3;++i)assert(record_ring_push(&q,(struct log_record){(uint32_t)i,i}));assert(!record_ring_push(&q,(struct log_record){4U,4}));assert(record_ring_pop(&q,&out)&&out.value==1);assert(record_ring_push(&q,(struct log_record){4U,4}));for(int32_t i=2;i<=4;++i)assert(record_ring_pop(&q,&out)&&out.value==i);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
