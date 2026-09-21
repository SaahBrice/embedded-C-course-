# Hide Library Internals

## Your task

Define the interface in `task.c` so this rule holds: Consumers can name only the opaque queue type; storage sizing and every invariant remain owned by the implementation. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **public header, private header, opaque state** into behavior a caller can verify. In firmware, a defect in `record_queue_required_bytes`, `record_queue_init`, `record_queue_push`, `record_queue_pop` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `record_queue_required_bytes`, `record_queue_init`, `record_queue_push`, `record_queue_pop`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
typedef struct record_queue record_queue_t;
size_t record_queue_required_bytes(void);
bool record_queue_init(void *storage, size_t storage_size, record_queue_t **out_queue);
bool record_queue_push(record_queue_t *queue, uint8_t value);
bool record_queue_pop(record_queue_t *queue, uint8_t *out_value);
```

Do not change these declarations.

- `record_queue_required_bytes` return type `size_t`: returns the result or status defined by the required behavior.
- `storage` from `void *storage`: pointer to caller-owned state that the function may update.
- `storage_size` from `size_t storage_size`: an input value; its meaningful range is demonstrated below.
- `out_queue` from `record_queue_t **out_queue`: caller-owned destination written only when the operation succeeds.
- `record_queue_init` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `queue` from `record_queue_t *queue`: pointer to caller-owned state that the function may update.
- `value` from `uint8_t value`: an input value; its meaningful range is demonstrated below.
- `record_queue_push` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `queue` from `record_queue_t *queue`: pointer to caller-owned state that the function may update.
- `out_value` from `uint8_t *out_value`: caller-owned destination written only when the operation succeeds.
- `record_queue_pop` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
unsigned char storage[128]; record_queue_t *q=NULL; assert(record_queue_required_bytes()<=sizeof storage); assert(record_queue_init(storage,sizeof storage,&q)); uint8_t out=0U; assert(record_queue_push(q,42U)); assert(record_queue_pop(q,&out)&&out==42U); assert(!record_queue_pop(q,&out)); assert(!record_queue_init(storage,1U,&q));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
