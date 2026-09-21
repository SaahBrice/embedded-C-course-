# Diagnose a Firmware Fault with GDB

## Your task

Define the interface in `task.c` so this rule holds: The repaired loop touches exactly the live array range; a watchpoint would show only matching elements being changed. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **backtrace, watchpoint, memory examine** into behavior a caller can verify. In firmware, a defect in `replace_value` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `replace_value`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
size_t replace_value(int32_t *values, size_t count, int32_t target, int32_t replacement);
```

Do not change these declarations.

- `values` from `int32_t *values`: pointer to caller-owned state that the function may update.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `target` from `int32_t target`: an input value; its meaningful range is demonstrated below.
- `replacement` from `int32_t replacement`: an input value; its meaningful range is demonstrated below.
- `replace_value` return type `size_t`: returns the result or status defined by the required behavior.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
int32_t v[]={1,2,1,3}; assert(replace_value(v,4U,1,9)==2U); assert(v[0]==9&&v[1]==2&&v[2]==9&&v[3]==3); assert(replace_value(v,0U,9,0)==0U); assert(replace_value(NULL,4U,1,2)==0U);
```

## Expected failure behavior

Produce exactly the documented value for every accepted input. Any rejected operation must use its documented status without undefined behavior or a partial state update.
