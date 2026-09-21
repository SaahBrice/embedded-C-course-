# Capstone: Integrate the Logger

## Your task

Define the interface in `task.c` so this rule holds: The integrated logger validates before commit, timestamps and queues accepted samples, persists each record once, retries transport within a bound, and retains ownership after failure. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **acquisition, validation, buffer, storage, transport** into behavior a caller can verify. In firmware, a defect in `logger_io`, `uint32_t`, `logger_io`, `logger_io`, `logger_init`, `logger_capture`, `logger_flush_one` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `logger_io`, `uint32_t`, `logger_io`, `logger_io`, `logger_init`, `logger_capture`, `logger_flush_one`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

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

Do not change these declarations.

- `void` from `*read)(void *`: pointer to caller-owned state that the function may update.
- `int32_t` from `int32_t *`: pointer to caller-owned state that the function may update.
- `logger_io` return type `enum`: returns one of the named status or state values declared above.
- `void` from `*store)(void *`: pointer to caller-owned state that the function may update.
- `uint8_t` from `const uint8_t *`: read-only input accessed through a pointer; null handling follows the contract.
- `size_t` from `size_t`: an input value; its meaningful range is demonstrated below.
- `logger_io` return type `enum`: returns one of the named status or state values declared above.
- `void` from `*send)(void *`: pointer to caller-owned state that the function may update.
- `uint8_t` from `const uint8_t *`: read-only input accessed through a pointer; null handling follows the contract.
- `size_t` from `size_t`: an input value; its meaningful range is demonstrated below.
- `logger_io` return type `enum`: returns one of the named status or state values declared above.
- `logger` from `struct integrated_logger *logger`: pointer to caller-owned state that the function may update.
- `ports` from `const struct logger_ports *ports`: read-only input accessed through a pointer; null handling follows the contract.
- `retry_limit` from `unsigned retry_limit`: an input value; its meaningful range is demonstrated below.
- `logger_init` return type `enum logger_result`: returns one of the named status or state values declared above.
- `logger` from `struct integrated_logger *logger`: pointer to caller-owned state that the function may update.
- `logger_capture` return type `enum logger_result`: returns one of the named status or state values declared above.
- `logger` from `struct integrated_logger *logger`: pointer to caller-owned state that the function may update.
- `logger_flush_one` return type `enum logger_result`: returns one of the named status or state values declared above.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct integration_fake f={21000,77U,LOGGER_IO_OK,LOGGER_IO_OK,{LOGGER_IO_TEMPORARY,LOGGER_IO_OK},2U,0U,0U,0U};
struct logger_ports ports={&f,integration_read,integration_now,integration_store,integration_send}; struct integrated_logger logger;
assert(logger_init(&logger,&ports,1U)==LOGGER_OK); assert(logger_capture(&logger)==LOGGER_OK&&logger.count==1U&&logger.next_sequence==1U);
assert(logger_flush_one(&logger)==LOGGER_OK&&logger.count==0U&&f.store_calls==1U&&f.send_calls==2U);
f.value=125001; assert(logger_capture(&logger)==LOGGER_RANGE&&logger.count==0U); f.value=42; f.read_result=LOGGER_IO_TEMPORARY; assert(logger_capture(&logger)==LOGGER_SENSOR_FAILURE);
f.read_result=LOGGER_IO_OK; assert(logger_capture(&logger)==LOGGER_OK); f.store_result=LOGGER_IO_TEMPORARY; assert(logger_flush_one(&logger)==LOGGER_STORAGE_FAILURE&&logger.count==1U);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
