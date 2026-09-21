# Final Release: Portable Data Logger

## What you are doing

Package, test, document, and release the reusable data-logger core with a clear STM32 adapter path. In this version of the exercise you learn by changing and running real C artifacts; there is no reflection or essay to submit.

## Why firmware engineers care

The key ideas are **library, host demo, STM32 adapter, documentation, version**. Firmware must keep behaving at boundaries and after unusual inputs, not merely in one demonstration. This exercise turns those ideas into behavior the compiler and tests can observe.

## Files you will edit

Edit `task.c` (keep the public declarations in `task.h` unchanged). Do not edit files below `curriculum/` or the hidden acceptance harness. Your personal copy is inside the attempt workspace printed by `./learn status`.

## Required behavior

The capstone release validates a versioned record shape, hashes exactly the serialized bytes, and accepts a record only when structure and integrity evidence both pass.

## Interface you must preserve

```c
bool logger_record_shape_valid(const uint8_t *bytes, size_t length);
uint32_t logger_release_checksum(const uint8_t *bytes, size_t length);
bool logger_release_validate(const uint8_t *bytes, size_t length, uint32_t expected_checksum);
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
