# Capstone: Inject Time

## Your task

Define the interface in `task.c` so this rule holds: Time is injected as a function plus context, making exact timestamps deterministic in tests and independent of a hardware clock. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **clock port, monotonic time, test determinism** into behavior a caller can verify. In firmware, a defect in `uint32_t`, `timestamp_record` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `uint32_t`, `timestamp_record`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
typedef uint32_t (*clock_now_fn)(void *context);
struct timestamped_value { uint32_t timestamp_ms; int32_t value; };
bool timestamp_record(clock_now_fn now, void *context, int32_t value, struct timestamped_value *out_record);
```

Do not change these declarations.

- `context` from `*clock_now_fn)(void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `uint32_t` return type `typedef`: returns the result or status defined by the required behavior.
- `now` from `clock_now_fn now`: an input value; its meaningful range is demonstrated below.
- `context` from `void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `value` from `int32_t value`: an input value; its meaningful range is demonstrated below.
- `out_record` from `struct timestamped_value *out_record`: caller-owned destination written only when the operation succeeds.
- `timestamp_record` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint32_t clock=1234U; struct timestamped_value r={0U,0}; assert(timestamp_record(fake_clock,&clock,-7,&r)&&r.timestamp_ms==1234U&&r.value==-7); assert(!timestamp_record(NULL,&clock,1,&r));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
