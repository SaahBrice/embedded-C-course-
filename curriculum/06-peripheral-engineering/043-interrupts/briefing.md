# Keep Interrupt Work Bounded

## Your task

Define the interface in `task.c` so this rule holds: The interrupt callback performs one bounded mailbox write, never overwrites a pending event, and foreground code explicitly consumes ownership. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **ISR, shared state, latency** into behavior a caller can verify. In firmware, a defect in `interrupt_capture`, `interrupt_take` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `interrupt_capture`, `interrupt_take`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
struct interrupt_mailbox { uint32_t event; bool pending; };
void interrupt_capture(void *context, uint32_t event);
bool interrupt_take(struct interrupt_mailbox *mailbox, uint32_t *out_event);
```

Do not change these declarations.

- `context` from `void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `event` from `uint32_t event`: an input value; its meaningful range is demonstrated below.
- `interrupt_capture` return type `void`: returns no value; the observable result is a state change.
- `mailbox` from `struct interrupt_mailbox *mailbox`: pointer to caller-owned state that the function may update.
- `out_event` from `uint32_t *out_event`: caller-owned destination written only when the operation succeeds.
- `interrupt_take` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct interrupt_mailbox box={0U,false}; uint32_t event=0U; interrupt_capture(&box,7U); assert(interrupt_take(&box,&event)&&event==7U); assert(!interrupt_take(&box,&event));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
