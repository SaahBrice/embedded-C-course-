# Level 11: Sensor Data-Logger Capstone

## Main objective

Combine the course into a portable, allocation-free sensor data logger with deterministic adapters and failure handling.

## What you should know before starting

Complete Level 10; this level builds directly on its C contracts and debugging habits.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Final Release: Portable Data Logger**.

## What you will build and learn

- Turn requirements into injected sensor, time, storage, and transport interfaces
- Validate, buffer, serialize, persist, and retry records without dynamic allocation
- Release a portable data logger with deterministic failure-injection tests

## Ordered sublevels

1. **Capstone: Define the Product** (`capstone-requirements`) — Implement `logger_requirements_valid`: Logger requirements enforce a nonzero period, at most ten-percent jitter, and a bounded static record capacity.
2. **Capstone: Partition the System** (`capstone-architecture`) — Implement `logger_ports_ready`: Initialization succeeds only when all four injected hardware boundaries are present.
3. **Capstone: Sensor Port** (`sensor-interface`) — Implement `sensor_status`, `sensor_read_checked`: The sensor port preserves unavailable and range failures as different statuses and commits only a validated reading.
4. **Capstone: Validate Samples** (`sample-validation`) — Implement `sample_valid`: A whole record is accepted only when every field is within its inclusive physical range; no partial state is committed.
5. **Capstone: Inject Time** (`timestamp-injection`) — Implement `uint32_t`, `timestamp_record`: Time is injected as a function plus context, making exact timestamps deterministic in tests and independent of a hardware clock.
6. **Capstone: Buffer Records** (`record-buffer`) — Implement `record_ring_push`, `record_ring_pop`: The fixed-capacity ring rejects new records when full and retains FIFO ownership across physical wraparound.
7. **Capstone: Serialize Deterministically** (`record-serialization`) — Implement `record_serialize`: `record_serialize` emits an explicit version byte and little-endian fields, independent of structure padding and host byte order.
8. **Capstone: Persist Records** (`storage-interface`) — Implement `size_t`, `storage_write_all`: The orchestration retains ownership until every byte is acknowledged, supports valid partial writes, and stops on zero progress.
9. **Capstone: Export Reliably** (`transport-retry`) — Implement `transport_status`, `transport_retry`: Only temporary failures are retried, the bound is exact and observable, and permanent failure returns immediately.
10. **Capstone: Integrate the Logger** (`data-logger-integration`) — Implement `logger_io`, `uint32_t`, `logger_io`, `logger_io`, `logger_init`, `logger_capture`, `logger_flush_one`: The integrated logger validates before commit, timestamps and queues accepted samples, persists each record once, retries transport within a bound, and retains ownership after failure.
11. **Final Release: Portable Data Logger** (`data-logger-release`) — FINAL BATTLE — Implement `logger_record_shape_valid`, `logger_release_checksum`, `logger_release_validate`: The capstone release validates a versioned record shape, hashes exactly the serialized bytes, and accepts a record only when structure and integrity evidence both pass.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **requirements and injected ports** is practised in: Capstone: Define the Product, Capstone: Partition the System, Capstone: Sensor Port, Capstone: Validate Samples, Capstone: Inject Time, Capstone: Integrate the Logger, Final Release: Portable Data Logger
- **buffering, serialization, and persistence** is practised in: Capstone: Buffer Records, Capstone: Serialize Deterministically, Capstone: Persist Records, Capstone: Export Reliably, Capstone: Integrate the Logger, Final Release: Portable Data Logger
- **failure handling and integrated release** is practised in: Capstone: Sensor Port, Capstone: Validate Samples, Capstone: Persist Records, Capstone: Export Reliably, Capstone: Integrate the Logger, Final Release: Portable Data Logger

## Final battle

**Final Release: Portable Data Logger** is the last required sublevel. It integrates **Capstone: Define the Product**, **Capstone: Serialize Deterministically**, **Capstone: Integrate the Logger**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
