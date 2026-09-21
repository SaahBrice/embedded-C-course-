# Separate Interface from Implementation

## Your task

Define the interface in `task.c` so this rule holds: `task.h` is self-contained and exposes one external declaration; the separate immutable harness is its consumer translation unit. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **headers, translation units, linkage** into behavior a caller can verify. In firmware, a defect in `crc8_update` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `crc8_update`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
uint8_t crc8_update(uint8_t crc, uint8_t byte);
```

Do not change these declarations.

- `crc` from `uint8_t crc`: an input value; its meaningful range is demonstrated below.
- `byte` from `uint8_t byte`: an input value; its meaningful range is demonstrated below.
- `crc8_update` return type `uint8_t`: returns the result or status defined by the required behavior.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(crc8_update(0U, 0U) == 0U); assert(crc8_update(0U, UINT8_C(0x31)) == UINT8_C(0x97)); assert(crc8_update(UINT8_C(0x5a), UINT8_C(0xc3)) == UINT8_C(0xc6));
```

## Expected failure behavior

Produce exactly the documented value for every accepted input. Any rejected operation must use its documented status without undefined behavior or a partial state update.
