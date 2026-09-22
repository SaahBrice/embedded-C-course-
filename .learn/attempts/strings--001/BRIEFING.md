# Handle C Strings Explicitly

## Your task

Define the interface in `task.c` so this rule holds: `buffer_append` first proves that the destination is terminated within capacity and commits only when suffix plus terminator fits. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **null terminator, buffer capacity, string APIs** into behavior a caller can verify. In firmware, a defect in `buffer_append` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The starter calls `strcat` without proving that the destination is terminated or that the suffix and final null byte fit. Replace that unbounded write with the checked contract described below.

## Read the function signature

```c
bool buffer_append(char *destination, size_t capacity, const char *suffix);
```

Do not change these declarations.

- `destination` from `char *destination`: pointer to caller-owned state that the function may update.
- `capacity` from `size_t capacity`: number of elements or bytes available; zero is a boundary case.
- `suffix` from `const char *suffix`: read-only input accessed through a pointer; null handling follows the contract.
- `buffer_append` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
char a[8] = "AB"; assert(buffer_append(a, sizeof a, "CDE") && strcmp(a, "ABCDE") == 0);
char b[5] = "AB"; assert(!buffer_append(b, sizeof b, "CDE") && strcmp(b, "AB") == 0);
char c[1] = {0}; assert(buffer_append(c, sizeof c, "") && c[0] == '\0');
char d[3] = {'A','B','C'}; assert(!buffer_append(d, sizeof d, "x"));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
