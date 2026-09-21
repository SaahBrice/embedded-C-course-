# Inject Behavior with Callbacks

## Your task

Define the interface in `task.c` so this rule holds: A registered callback is checked, invoked exactly once, and receives the caller-owned context unchanged. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **function pointers, context pointer, ownership** into behavior a caller can verify. In firmware, a defect in `bool`, `callback_run_once` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `bool`, `callback_run_once`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
typedef bool (*status_callback)(void *context, uint8_t value);
bool callback_run_once(status_callback callback, void *context, uint8_t value);
```

Do not change these declarations.

- `context` from `*status_callback)(void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `value` from `uint8_t value`: an input value; its meaningful range is demonstrated below.
- `bool` return type `typedef`: returns the result or status defined by the required behavior.
- `callback` from `status_callback callback`: an input value; its meaningful range is demonstrated below.
- `context` from `void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `value` from `uint8_t value`: an input value; its meaningful range is demonstrated below.
- `callback_run_once` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
unsigned total=1U; assert(callback_run_once(capture_status,&total,4U)&&total==5U); assert(!callback_run_once(NULL,&total,3U)&&total==5U);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
