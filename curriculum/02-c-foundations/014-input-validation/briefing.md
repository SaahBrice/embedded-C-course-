# Validate External Input

## Your task

Define the interface in `task.c` so this rule holds: The parser accepts the complete decimal string only, checks conversion errors and range, and never accepts a negative value. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **strtol, end pointers, range checks** into behavior a caller can verify. In firmware, a defect in `parse_u16` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `parse_u16`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool parse_u16(const char *text, uint16_t *out_value);
```

Do not change these declarations.

- `text` from `const char *text`: read-only input accessed through a pointer; null handling follows the contract.
- `out_value` from `uint16_t *out_value`: caller-owned destination written only when the operation succeeds.
- `parse_u16` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint16_t value = 9U; assert(parse_u16("0", &value) && value == 0U); assert(parse_u16("65535", &value) && value == 65535U); assert(!parse_u16("65536", &value)); assert(!parse_u16("-1", &value)); assert(!parse_u16("12x", &value)); assert(!parse_u16("", &value));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
