# Treat Warnings as Defects

## Your task

The function converts a raw reading from a 12-bit ADC into millivolts. A 12-bit ADC code can be **0 through 4095**. `reference_mv` is the voltage, in millivolts, represented by the maximum code. The calculation is approximately:

```text
millivolts = code * reference_mv / 4095
```

The starter looks close, but embedded C arithmetic happens in fixed-width integer types. You must validate the inputs and make the multiplication happen as `uint32_t` arithmetic so the intermediate result cannot wrap before division.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

ADC conversion code sits directly between electrical measurements and control decisions. An unnoticed narrowing or invalid raw code can turn into a believable but wrong voltage, so strict conversion warnings and explicit range checks are treated as defects rather than cosmetic messages.

The starter checks only whether `out_mv` is null. It does not reject an impossible ADC code above 4095 or a zero reference voltage. It also performs the multiplication without explicitly widening an operand first.

## Read the function signature

```c
bool adc_to_millivolts(uint16_t code, uint16_t reference_mv, uint16_t *out_mv);
```

Do not change this declaration.

- `code` is the raw 12-bit ADC result.
- `reference_mv` is the millivolt value represented by full scale.
- `out_mv` points to the caller's destination and is written only on success.
- The function returns `true` after storing a valid result; otherwise it returns `false`.

## Concrete examples

- `code = 0`, `reference_mv = 3300` → return `true` and store `0` in `*out_mv`.
- `code = 4095`, `reference_mv = 3300` → return `true` and store `3300`.
- `code = 4096` → return `false` because it is outside a 12-bit ADC's range.
- `reference_mv = 0` → return `false`.
- `out_mv = NULL` → return `false`; there is nowhere safe to store the answer.

On every failure, the function must not write through `out_mv`. A successful calculation should use a `uint32_t` intermediate before narrowing the final, known-to-fit result to `uint16_t`.

## Expected failure behavior

Reject a code above 4095, a zero reference voltage, or a null output pointer by returning `false`. Check all three before writing through `out_mv`, so a failed call cannot overwrite the caller's previous value. Accepted inputs return `true` only after the complete millivolt result has been stored.
