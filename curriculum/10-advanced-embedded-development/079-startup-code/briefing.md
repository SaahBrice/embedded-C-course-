# Follow MCU Startup

## Your task

Define the interface in `task.c` so this rule holds: Startup zeroes exactly the BSS word range and permits an empty range without dereferencing null. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **reset handler, vector table, C runtime** into behavior a caller can verify. In firmware, a defect in `zero_bss_words` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `zero_bss_words`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool zero_bss_words(uint32_t *words, size_t count);
```

Do not change these declarations.

- `words` from `uint32_t *words`: pointer to caller-owned state that the function may update.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `zero_bss_words` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint32_t words[]={1U,2U,3U}; assert(zero_bss_words(words,3U)&&words[0]==0U&&words[2]==0U); assert(zero_bss_words(NULL,0U)); assert(!zero_bss_words(NULL,1U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
