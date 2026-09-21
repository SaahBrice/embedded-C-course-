# Decode Binary and Hexadecimal

## Your task

Define the interface in `task.c` so this rule holds: The high and low four-bit nibbles exchange positions without changing any bit. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **base conversion, bit positions, hex notation** into behavior a caller can verify. In firmware, a defect in `swap_nibbles` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `swap_nibbles`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
uint8_t swap_nibbles(uint8_t value);
```

Do not change these declarations.

- `value` from `uint8_t value`: an input value; its meaningful range is demonstrated below.
- `swap_nibbles` return type `uint8_t`: returns the result or status defined by the required behavior.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(swap_nibbles(UINT8_C(0xa5))==UINT8_C(0x5a)); assert(swap_nibbles(UINT8_C(0xf0))==UINT8_C(0x0f)); assert(swap_nibbles(0U)==0U);
```

## Expected failure behavior

Produce exactly the documented value for every accepted input. Any rejected operation must use its documented status without undefined behavior or a partial state update.
