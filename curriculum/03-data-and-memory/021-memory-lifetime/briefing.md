# Prevent Lifetime Defects

## Your task

Define the interface in `task.c` so this rule holds: The function copies a live value into caller-owned storage instead of returning or retaining a pointer to temporary storage. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **automatic storage, static storage, dangling pointers** into behavior a caller can verify. In firmware, a defect in `snapshot_i16` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `snapshot_i16`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool snapshot_i16(const int16_t *source, int16_t *destination);
```

Do not change these declarations.

- `source` from `const int16_t *source`: read-only input accessed through a pointer; null handling follows the contract.
- `destination` from `int16_t *destination`: pointer to caller-owned state that the function may update.
- `snapshot_i16` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
int16_t source=-7,destination=4; assert(snapshot_i16(&source,&destination)&&destination==-7); source=12; assert(destination==-7); assert(!snapshot_i16(NULL,&destination)); assert(!snapshot_i16(&source,NULL));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
