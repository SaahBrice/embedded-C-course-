# Use the Preprocessor Carefully

## Your task

Define the interface in `task.c` so this rule holds: An inline-style function evaluates its argument once and widens before multiplication, avoiding unsafe square macros. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **include guards, macros, conditional compilation** into behavior a caller can verify. In firmware, a defect in `square_i16_once` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `square_i16_once`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
int32_t square_i16_once(int16_t value);
```

Do not change these declarations.

- `value` from `int16_t value`: an input value; its meaningful range is demonstrated below.
- `square_i16_once` return type `int32_t`: returns the result or status defined by the required behavior.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(square_i16_once(0)==0); assert(square_i16_once(-3)==9); assert(square_i16_once(INT16_MAX)==INT32_C(1073676289)); assert(square_i16_once(INT16_MIN)==INT32_C(1073741824));
```

## Expected failure behavior

Produce exactly the documented value for every accepted input. Any rejected operation must use its documented status without undefined behavior or a partial state update.
