# Transact over SPI

## Your task

Define the interface in `task.c` so this rule holds: The portable transaction builder sets the protocol read bit and dummy byte only after validating address and capacity. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **clock polarity, phase, chip select, full duplex** into behavior a caller can verify. In firmware, a defect in `spi_build_read` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `spi_build_read`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool spi_build_read(uint8_t register_address, uint8_t *transaction, size_t capacity, size_t *out_length);
```

Do not change these declarations.

- `register_address` from `uint8_t register_address`: an input value; its meaningful range is demonstrated below.
- `transaction` from `uint8_t *transaction`: pointer to caller-owned state that the function may update.
- `capacity` from `size_t capacity`: number of elements or bytes available; zero is a boundary case.
- `out_length` from `size_t *out_length`: caller-owned destination written only when the operation succeeds.
- `spi_build_read` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint8_t tx[2]={0U}; size_t n=0U; assert(spi_build_read(0x12U,tx,2U,&n)&&n==2U&&tx[0]==0x92U&&tx[1]==0xffU); assert(!spi_build_read(0x80U,tx,2U,&n)); assert(!spi_build_read(1U,tx,1U,&n));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
