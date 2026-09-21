# Capstone: Export Reliably

## Your task

Define the interface in `task.c` so this rule holds: Only temporary failures are retried, the bound is exact and observable, and permanent failure returns immediately. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **transport port, bounded retry, backoff** into behavior a caller can verify. In firmware, a defect in `transport_status`, `transport_retry` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `transport_status`, `transport_retry`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
enum transport_status { TRANSPORT_OK, TRANSPORT_TEMPORARY, TRANSPORT_PERMANENT };
typedef enum transport_status (*transport_send_fn)(void *context);
enum transport_status transport_retry(transport_send_fn send, void *context, unsigned max_attempts, unsigned *out_attempts);
```

Do not change these declarations.

- `context` from `*transport_send_fn)(void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `transport_status` return type `typedef enum`: returns one of the named status or state values declared above.
- `send` from `transport_send_fn send`: an input value; its meaningful range is demonstrated below.
- `context` from `void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `max_attempts` from `unsigned max_attempts`: an input value; its meaningful range is demonstrated below.
- `out_attempts` from `unsigned *out_attempts`: caller-owned destination written only when the operation succeeds.
- `transport_retry` return type `enum transport_status`: returns one of the named status or state values declared above.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct fake_transport t={2U,0U,TRANSPORT_OK}; unsigned n=0U; assert(transport_retry(fake_transport_send,&t,4U,&n)==TRANSPORT_OK&&n==3U); t.temporary_left=9U;t.calls=0U;assert(transport_retry(fake_transport_send,&t,2U,&n)==TRANSPORT_TEMPORARY&&n==2U);t.temporary_left=0U;t.final=TRANSPORT_PERMANENT;assert(transport_retry(fake_transport_send,&t,4U,&n)==TRANSPORT_PERMANENT&&n==1U);
```

## Expected failure behavior

Return the named failure or safe-state enumerator for rejected work; never invent an out-of-range enum result or partially publish output.
