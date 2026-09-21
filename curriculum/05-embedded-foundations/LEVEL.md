# Level 5: Embedded Foundations

## Main objective

Connect portable C to CPU memory, exact-width values, register fields, qualifiers, electronics, and datasheets.

## What you should know before starting

Complete Level 4; this level builds directly on its C contracts and debugging habits.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Release: Register-Level GPIO Driver**.

## What you will build and learn

- Relate C expressions and qualifiers to CPU, memory, and peripheral-register behavior
- Build masks and exact-width operations from electronics and datasheet constraints
- Release a register-level GPIO configuration driver

## Ordered sublevels

1. **Map CPU and Memory Responsibilities** (`cpu-memory-model`) — Implement `load_modify_value`: The returned value models the CPU's load-modify phase while preserving bits outside the requested masks.
2. **Use Fixed-Width Integers** (`fixed-width-integers`) — Implement `saturating_counter_add`: The counter has an exact 32-bit representation and saturates instead of wrapping at its maximum wire value.
3. **Manipulate Register Bits** (`register-masks`) — Implement `register_field_write`: The field value is validated against the shifted mask before a clear-and-set update preserves all unrelated bits.
4. **Apply const and volatile Correctly** (`const-and-volatile`) — Implement `sample_volatile_register`: The pointer prevents writes through this view while volatile preserves the observable register read.
5. **Model Memory-Mapped I/O** (`memory-mapped-io`) — Implement `register_update`: The volatile register is read once and written once; the pure mask calculation between those observable accesses is explicit.
6. **Connect Firmware to Electronics** (`electronics-basics`) — Implement `led_output_level`: The logical LED request is converted to the correct electrical output level for active-high or active-low wiring.
7. **Read a Peripheral Datasheet** (`datasheet-reading`) — Implement `datasheet_field_encode`: A value is proven to fit a datasheet field before shifting and masking it into register position.
8. **Release: Register-Level GPIO Driver** (`register-driver-release`) — FINAL BATTLE — Implement `gpio_pin_valid`, `gpio_mode_set`, `gpio_mode_matches`: The register-driver release validates the pin domain, performs a reserved-bit-preserving field update, and reads the configured field back through a separate query.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **fixed-width register arithmetic** is practised in: Map CPU and Memory Responsibilities, Use Fixed-Width Integers, Manipulate Register Bits, Apply const and volatile Correctly, Model Memory-Mapped I/O, Read a Peripheral Datasheet, Release: Register-Level GPIO Driver
- **qualifiers and hardware access** is practised in: Map CPU and Memory Responsibilities, Manipulate Register Bits, Apply const and volatile Correctly, Model Memory-Mapped I/O, Connect Firmware to Electronics, Release: Register-Level GPIO Driver
- **datasheet-driven driver design** is practised in: Use Fixed-Width Integers, Manipulate Register Bits, Model Memory-Mapped I/O, Connect Firmware to Electronics, Read a Peripheral Datasheet, Release: Register-Level GPIO Driver

## Final battle

**Release: Register-Level GPIO Driver** is the last required sublevel. It integrates **Manipulate Register Bits**, **Model Memory-Mapped I/O**, **Read a Peripheral Datasheet**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
