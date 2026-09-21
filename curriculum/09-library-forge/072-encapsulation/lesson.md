# Hide Library Internals

## What you are doing

Move implementation details out of the consumer-visible interface without changing behavior. In this version of the exercise you learn by changing and running real C artifacts; there is no reflection or essay to submit.

## Why firmware engineers care

The key ideas are **public header, private header, opaque state**. Firmware must keep behaving at boundaries and after unusual inputs, not merely in one demonstration. This exercise turns those ideas into behavior the compiler and tests can observe.

## Files you will edit

Edit `task.c` (keep the public declarations in `task.h` unchanged). Do not edit files below `curriculum/` or the hidden acceptance harness. Your personal copy is inside the attempt workspace printed by `./learn status`.

## Required behavior

Consumers can name only the opaque queue type; storage sizing and every invariant remain owned by the implementation.

## Interface you must preserve

```c
typedef struct record_queue record_queue_t;
size_t record_queue_required_bytes(void);
bool record_queue_init(void *storage, size_t storage_size, record_queue_t **out_queue);
bool record_queue_push(record_queue_t *queue, uint8_t value);
bool record_queue_pop(record_queue_t *queue, uint8_t *out_value);
```

## A practical way to begin

1. Read the complete starter and public interface before changing it.
2. Find the placeholder or deliberate defect and predict the first failing case.
3. Make the smallest correct change while keeping strict compiler warnings enabled.
4. Run `./learn test` and address the first useful diagnostic.
5. Check the zero/empty case, an ordinary case, and the first invalid or maximum case.

## Common mistake

Do not weaken the function signature, compiler flags, error result, or bounds just to make one example work. A passing implementation must preserve the contract for callers that you cannot see.

## Success looks like

Implement the declared C interface so every normal, boundary, and invalid case in the immutable harness passes. Run `./learn test`; every required check must report `PASS`. Use `./learn solution` whenever you need the worked implementation—solutions carry no penalty.
