# Level 4: Professional C

## Main objective

Build portable multi-file C modules with defensive interfaces, explicit errors, defined behavior, and typed dispatch.

## What you should know before starting

Complete Level 3; this level builds directly on its C contracts and debugging habits.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Release: Portable CRC Module**.

## What you will build and learn

- Separate declarations and definitions across translation units
- Design portable defensive interfaces with meaningful error results and defined behavior
- Release a reusable CRC module behind a stable public header

## Ordered sublevels

1. **Separate Interface from Implementation** (`headers-and-linking`) — Implement `crc8_update`: `task.h` is self-contained and exposes one external declaration; the separate immutable harness is its consumer translation unit.
2. **Use the Preprocessor Carefully** (`preprocessor-discipline`) — Implement `square_i16_once`: An inline-style function evaluates its argument once and widens before multiplication, avoiding unsafe square macros.
3. **Design Defensive APIs** (`defensive-apis`) — Implement `bounded_copy`: Null pointers are legal only for a zero-length operation, capacity is checked before the first write, and failure leaves storage untouched.
4. **Propagate Errors Without Guessing** (`error-models`) — Implement `sensor_scale`: Distinct argument and range statuses propagate meaning; the numeric output is written only on success.
5. **Recognize Undefined Behavior** (`undefined-behavior`) — Implement `safe_left_shift`: The shift count is narrower than the type width and the value is proven representable before the shift expression executes.
6. **Write Portable C** (`portability`) — Implement `read_u32_le`: Byte-wise decoding avoids alignment, padding, host-endianness, and aliasing assumptions.
7. **Dispatch with Function Pointers** (`function-pointers`) — Implement `bool`, `event_dispatch`: Dispatch validates table bounds and the selected callback before invoking it with the caller-owned context pointer.
8. **Release: Portable CRC Module** (`modular-library-release`) — FINAL BATTLE — Implement `crc8_update`, `crc8`, `crc8_verify`: The library release exposes a one-byte primitive, a counted-buffer operation, and a verification API through one self-contained header and separately compiled implementation.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **public interfaces and translation units** is practised in: Separate Interface from Implementation, Use the Preprocessor Carefully, Design Defensive APIs, Propagate Errors Without Guessing, Dispatch with Function Pointers, Release: Portable CRC Module
- **validation, errors, and defined behavior** is practised in: Design Defensive APIs, Propagate Errors Without Guessing, Recognize Undefined Behavior, Write Portable C, Release: Portable CRC Module
- **portable operations and typed dispatch** is practised in: Separate Interface from Implementation, Recognize Undefined Behavior, Write Portable C, Dispatch with Function Pointers, Release: Portable CRC Module

## Final battle

**Release: Portable CRC Module** is the last required sublevel. It integrates **Separate Interface from Implementation**, **Design Defensive APIs**, **Propagate Errors Without Guessing**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
