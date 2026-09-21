# Prepare the STM32 Toolchain

## Your task

Define the interface in `task.c` so this rule holds: The compiled artifact is accepted only when its ELF magic and machine field identify a little-endian ARM target. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **ARM compiler, debug probe, OpenOCD, Cube tools** into behavior a caller can verify. In firmware, a defect in `elf_header_targets_arm` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `elf_header_targets_arm`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool elf_header_targets_arm(const uint8_t *header, size_t length);
```

Do not change these declarations.

- `header` from `const uint8_t *header`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `elf_header_targets_arm` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const uint8_t arm[20]={0x7fU,'E','L','F',0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0x28U,0U}; assert(elf_header_targets_arm(arm,20U)); assert(!elf_header_targets_arm(arm,19U)); uint8_t host[20]={0}; memcpy(host,arm,20U); host[18]=0x3eU; assert(!elf_header_targets_arm(host,20U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
