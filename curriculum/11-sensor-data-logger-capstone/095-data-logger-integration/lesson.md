# Capstone: Integrate the Logger

## What you are doing

Integrate the complete host logger and pass nominal plus injected-failure scenarios. In this version of the exercise you learn by changing and running real C artifacts; there is no reflection or essay to submit.

## Why firmware engineers care

The key ideas are **acquisition, validation, buffer, storage, transport**. Firmware must keep behaving at boundaries and after unusual inputs, not merely in one demonstration. This exercise turns those ideas into behavior the compiler and tests can observe.

## Files you will edit

Edit `task.c` (keep the public declarations in `task.h` unchanged). Do not edit files below `curriculum/` or the hidden acceptance harness. Your personal copy is inside the attempt workspace printed by `./learn status`.

## Required behavior

The integrated logger validates before commit, timestamps and queues accepted samples, persists each record once, retries transport within a bound, and retains ownership after failure.

## Interface you must preserve

```c
#define INTEGRATED_LOGGER_CAPACITY 2U
enum logger_io { LOGGER_IO_OK, LOGGER_IO_TEMPORARY, LOGGER_IO_PERMANENT };
enum logger_result { LOGGER_OK, LOGGER_ARGUMENT, LOGGER_SENSOR_FAILURE, LOGGER_RANGE, LOGGER_FULL, LOGGER_EMPTY, LOGGER_STORAGE_FAILURE, LOGGER_TRANSPORT_FAILURE };
struct logger_ports { void *context; enum logger_io (*read)(void *, int32_t *); uint32_t (*now)(void *); enum logger_io (*store)(void *, const uint8_t *, size_t); enum logger_io (*send)(void *, const uint8_t *, size_t); };
struct logger_slot { uint32_t sequence, timestamp; int32_t value; bool persisted; };
struct integrated_logger { struct logger_ports ports; struct logger_slot slots[INTEGRATED_LOGGER_CAPACITY]; size_t head, tail, count; uint32_t next_sequence; unsigned retry_limit; };
enum logger_result logger_init(struct integrated_logger *logger, const struct logger_ports *ports, unsigned retry_limit);
enum logger_result logger_capture(struct integrated_logger *logger);
enum logger_result logger_flush_one(struct integrated_logger *logger);
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
