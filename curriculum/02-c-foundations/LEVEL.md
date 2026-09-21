# Level 2: C Foundations

## Main objective

Control C values and program flow through deliberate types, expressions, decisions, loops, functions, and validated input.

## What you should know before starting

Complete Level 1; this level builds directly on its C contracts and debugging habits.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Release: Telemetry Converter**.

## What you will build and learn

- Choose C types that match the range and meaning of firmware data
- Write decisions, loops, functions, and validated conversions with explicit boundaries
- Release a checked telemetry conversion component

## Ordered sublevels

1. **Choose Integer Types Deliberately** (`integer-types`) — Implement `temperature_fits_i16`: The range check proves whether a signed 32-bit measurement can be represented by int16_t before narrowing.
2. **Measure Floating-Point Trade-offs** (`floating-point-tradeoffs`) — Implement `volts_to_millivolts`: Finite nonnegative volts in the documented range are rounded to integer millivolts; invalid ranges are rejected.
3. **Control Expression Evaluation** (`operators-expressions`) — Implement `status_bits_update`: The expression sets requested bits, clears requested bits last, and contains no hidden side effects.
4. **Route Fault States** (`decisions`) — Implement `classify_measurement`: Fault status has priority; otherwise the inclusive sensor range is accepted and out-of-range data is retried.
5. **Process a Sample Window** (`loops`) — Implement `sample_average`: The loop invariant is that `total` contains exactly the first `i` samples; an empty window has no average.
6. **Extract Testable Functions** (`functions`) — Implement `clamp_i32`: `clamp_i32` is a pure, independently testable calculation with explicit behavior for an invalid interval.
7. **Reason About Scope and Storage** (`scope-and-storage`) — Implement `instance_increment`: Caller-owned state keeps independent instances separate and refuses unsigned wraparound.
8. **Validate External Input** (`input-validation`) — Implement `parse_u16`: The parser accepts the complete decimal string only, checks conversion errors and range, and never accepts a negative value.
9. **Decompose a Firmware Ticket** (`decomposition`) — Implement `scale_offset_sample`: Parse-free transformation is decomposed into offset, widened scaling, range validation, and one final output commit.
10. **Release: Telemetry Converter** (`telemetry-cli-release`) — FINAL BATTLE — Implement `celsius_in_sensor_range`, `celsius_to_milli`, `telemetry_prepare`: The telemetry release validates the physical range, performs deterministic milli-degree conversion, and refuses to publish a measurement when the sensor reports a fault.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **numeric representation and safe arithmetic** is practised in: Choose Integer Types Deliberately, Measure Floating-Point Trade-offs, Control Expression Evaluation, Route Fault States, Process a Sample Window, Release: Telemetry Converter
- **control flow and decomposition** is practised in: Control Expression Evaluation, Route Fault States, Process a Sample Window, Extract Testable Functions, Decompose a Firmware Ticket, Release: Telemetry Converter
- **validated status-returning APIs** is practised in: Extract Testable Functions, Reason About Scope and Storage, Validate External Input, Decompose a Firmware Ticket, Release: Telemetry Converter

## Final battle

**Release: Telemetry Converter** is the last required sublevel. It integrates **Measure Floating-Point Trade-offs**, **Route Fault States**, **Validate External Input**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
