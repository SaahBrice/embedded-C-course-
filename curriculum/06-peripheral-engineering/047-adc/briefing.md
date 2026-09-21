# Acquire Analog Samples

## Your task

Define the interface in `task.c` so this rule holds: Resolution determines the maximum code; widened arithmetic and half-up rounding map only valid codes into millivolts. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **resolution, reference voltage, scaling** into behavior a caller can verify. In firmware, a defect in `adc_code_to_mv` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `adc_code_to_mv`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool adc_code_to_mv(uint16_t code, uint8_t resolution_bits, uint16_t reference_mv, uint16_t *out_mv);
```

Do not change these declarations.

- `code` from `uint16_t code`: an input value; its meaningful range is demonstrated below.
- `resolution_bits` from `uint8_t resolution_bits`: an input value; its meaningful range is demonstrated below.
- `reference_mv` from `uint16_t reference_mv`: an input value; its meaningful range is demonstrated below.
- `out_mv` from `uint16_t *out_mv`: caller-owned destination written only when the operation succeeds.
- `adc_code_to_mv` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint16_t mv=0U; assert(adc_code_to_mv(2048U,12U,3300U,&mv) && mv==1650U); assert(adc_code_to_mv(4095U,12U,3300U,&mv) && mv==3300U); assert(!adc_code_to_mv(4096U,12U,3300U,&mv));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
