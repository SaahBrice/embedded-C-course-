# Test C Modules in Isolation

## Your task

You are writing the test program in `test.c`, not implementing `median3`. The engine compiles your tests twice: once with a correct `median3` and once with a deliberately defective version. A useful test suite must accept the correct module and make the defective module fail.

Edit `test.c` and the supplied `task.h` in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. `./learn run` compiles `test.c` against both supplied modules and shows whether your tests distinguish them. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

A test that only runs is not necessarily useful: it must distinguish a correct module from a plausible defect. Firmware regressions often hide at ordering, duplicate-value, sign, and limit boundaries, so this sublevel makes the tests themselves the C artifact you design.

The starter `main` returns immediately and tests nothing. Add ordinary C assertions that cover different input orders, repeated values, negative values, and limits. Keep the public declaration in `task.h` unchanged.

## Read the function signature

```c
int16_t median3(int16_t a, int16_t b, int16_t c);
```

Do not change these declarations.

- `a` from `int16_t a`: an input value; its meaningful range is demonstrated below.
- `b` from `int16_t b`: an input value; its meaningful range is demonstrated below.
- `c` from `int16_t c`: an input value; its meaningful range is demonstrated below.
- `median3` return type `int16_t`: returns the result or status defined by the required behavior.

## Concrete examples

- `median3(1, 2, 3)` must be `2`, and changing the argument order must not change the median.
- `median3(7, 7, 2)` must be `7`.
- Include negative and limiting `int16_t` values so an implementation that merely returns one fixed argument cannot survive.

## Expected failure behavior

The test executable must return zero for the good module and fail for the defective module. A suite that rejects both—or accepts both—does not pass.
