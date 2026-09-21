# Map CPU and Memory Responsibilities

## Your task

Define the interface in `task.c` so this rule holds: The returned value models the CPU's load-modify phase while preserving bits outside the requested masks. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **registers, address space, load/store** into behavior a caller can verify. In firmware, a defect in `load_modify_value` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `load_modify_value`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
uint32_t load_modify_value(uint32_t loaded, uint32_t set_mask, uint32_t clear_mask);
```

Do not change these declarations.

- `loaded` from `uint32_t loaded`: an input value; its meaningful range is demonstrated below.
- `set_mask` from `uint32_t set_mask`: an input value; its meaningful range is demonstrated below.
- `clear_mask` from `uint32_t clear_mask`: an input value; its meaningful range is demonstrated below.
- `load_modify_value` return type `uint32_t`: returns the result or status defined by the required behavior.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(load_modify_value(UINT32_C(0xf0),UINT32_C(0x05),UINT32_C(0x30))==UINT32_C(0xc5)); assert(load_modify_value(0U,UINT32_C(0x80),0U)==UINT32_C(0x80));
```

## Expected failure behavior

Produce exactly the documented value for every accepted input. Any rejected operation must use its documented status without undefined behavior or a partial state update.
