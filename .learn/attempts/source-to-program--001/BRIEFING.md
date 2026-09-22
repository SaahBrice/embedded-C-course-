# Trace Source to Executable

## Your task

Define the interface in `task.c` so this rule holds: A separately declared function produces input plus one, rejects overflow, and writes output only on success. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **preprocessing, compilation, assembly, linking** into behavior a caller can verify. In firmware, a defect in `linked_increment` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `linked_increment`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool linked_increment(int32_t input, int32_t *out_value);
```

Do not change these declarations.

- `input` from `int32_t input`: an input value; its meaningful range is demonstrated below.
- `out_value` from `int32_t *out_value`: caller-owned destination written only when the operation succeeds.
- `linked_increment` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
int32_t out=0; assert(linked_increment(0,&out)&&out==1); assert(linked_increment(-2,&out)&&out==-1); assert(!linked_increment(INT32_MAX,&out)); assert(!linked_increment(1,NULL));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
