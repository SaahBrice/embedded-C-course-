# Dispatch with Function Pointers

## Your task

Define the interface in `task.c` so this rule holds: Dispatch validates table bounds and the selected callback before invoking it with the caller-owned context pointer. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **callback signatures, tables, null callbacks** into behavior a caller can verify. In firmware, a defect in `bool`, `event_dispatch` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `bool`, `event_dispatch`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
typedef bool (*event_handler)(void *context, uint8_t value);
bool event_dispatch(uint8_t event, event_handler const *handlers, size_t count, void *context, uint8_t value);
```

Do not change these declarations.

- `context` from `*event_handler)(void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `value` from `uint8_t value`: an input value; its meaningful range is demonstrated below.
- `bool` return type `typedef`: returns the result or status defined by the required behavior.
- `event` from `uint8_t event`: an input value; its meaningful range is demonstrated below.
- `handlers` from `event_handler const *handlers`: read-only input accessed through a pointer; null handling follows the contract.
- `count` from `size_t count`: number of elements or bytes available; zero is a boundary case.
- `context` from `void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `value` from `uint8_t value`: an input value; its meaningful range is demonstrated below.
- `event_dispatch` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
event_handler handlers[] = {capture_handler, NULL}; unsigned total = 0U;
assert(event_dispatch(0U,handlers,2U,&total,7U) && total == 7U); assert(!event_dispatch(1U,handlers,2U,&total,1U)); assert(!event_dispatch(2U,handlers,2U,&total,1U));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
