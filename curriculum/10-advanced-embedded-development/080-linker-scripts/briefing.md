# Read a Linker Script

## Your task

Define the interface in `task.c` so this rule holds: A section fits only when its complete address range lies within a linker memory region without overflow. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **MEMORY, SECTIONS, symbols** into behavior a caller can verify. In firmware, a defect in `region_contains` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `region_contains`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool region_contains(uint32_t origin, uint32_t length, uint32_t address, uint32_t size);
```

Do not change these declarations.

- `origin` from `uint32_t origin`: an input value; its meaningful range is demonstrated below.
- `length` from `uint32_t length`: number of elements or bytes available; zero is a boundary case.
- `address` from `uint32_t address`: an input value; its meaningful range is demonstrated below.
- `size` from `uint32_t size`: number of elements or bytes available; zero is a boundary case.
- `region_contains` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x20000000),16U)); assert(region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x200003f0),16U)); assert(!region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x1fffffff),1U)); assert(!region_contains(UINT32_C(0xfffffff0),32U,UINT32_C(0xfffffff0),32U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
