# Transact over I2C

## Your task

Define the interface in `task.c` so this rule holds: A seven-bit device address and the transfer direction remain separate until the bus address byte is formed. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **address, start stop, ACK NACK** into behavior a caller can verify. In firmware, a defect in `i2c_address_byte` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `i2c_address_byte`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool i2c_address_byte(uint8_t address_7bit, bool read, uint8_t *out_byte);
```

Do not change these declarations.

- `address_7bit` from `uint8_t address_7bit`: an input value; its meaningful range is demonstrated below.
- `read` from `bool read`: a true/false input flag.
- `out_byte` from `uint8_t *out_byte`: caller-owned destination written only when the operation succeeds.
- `i2c_address_byte` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint8_t byte=0U; assert(i2c_address_byte(0x48U,false,&byte)&&byte==0x90U); assert(i2c_address_byte(0x48U,true,&byte)&&byte==0x91U); assert(!i2c_address_byte(0x80U,true,&byte));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
