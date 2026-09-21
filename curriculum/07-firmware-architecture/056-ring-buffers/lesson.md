# Implement a Ring Buffer

## What you are doing

Implement a fixed-capacity byte ring with explicit full and empty results. In this version of the exercise you learn by changing and running real C artifacts; there is no reflection or essay to submit.

## Why firmware engineers care

The key ideas are **head, tail, full empty policy**. Firmware must keep behaving at boundaries and after unusual inputs, not merely in one demonstration. This exercise turns those ideas into behavior the compiler and tests can observe.

## Files you will edit

Edit `task.c` (keep the public declarations in `task.h` unchanged). Do not edit files below `curriculum/` or the hidden acceptance harness. Your personal copy is inside the attempt workspace printed by `./learn status`.

## Required behavior

Head owns the next write, tail owns the next read, count distinguishes full from empty, and push rejects new data when full.

## Interface you must preserve

```c
#define BYTE_RING_CAPACITY 4U
struct byte_ring { uint8_t data[BYTE_RING_CAPACITY]; size_t head, tail, count; };
bool byte_ring_push(struct byte_ring *ring, uint8_t value);
bool byte_ring_pop(struct byte_ring *ring, uint8_t *out_value);
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
