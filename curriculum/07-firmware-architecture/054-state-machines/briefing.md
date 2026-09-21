# Model Behavior as States

## Your task

Define the interface in `task.c` so this rule holds: `controller_transition` is total: every state/event pair has a deterministic result, and impossible states enter fault rather than guessing. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **state, event, transition, guard** into behavior a caller can verify. In firmware, a defect in `controller_transition` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `controller_transition`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
enum controller_state { CONTROLLER_IDLE, CONTROLLER_SAMPLING, CONTROLLER_FAULT };
enum controller_event { EVENT_START, EVENT_SAMPLE_OK, EVENT_SAMPLE_BAD, EVENT_RESET };
enum controller_state controller_transition(enum controller_state state, enum controller_event event);
```

Do not change these declarations.

- `state` from `enum controller_state state`: an input value; its meaningful range is demonstrated below.
- `event` from `enum controller_event event`: an input value; its meaningful range is demonstrated below.
- `controller_transition` return type `enum controller_state`: returns one of the named status or state values declared above.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(controller_transition(CONTROLLER_IDLE,EVENT_START)==CONTROLLER_SAMPLING); assert(controller_transition(CONTROLLER_SAMPLING,EVENT_SAMPLE_OK)==CONTROLLER_IDLE); assert(controller_transition(CONTROLLER_SAMPLING,EVENT_SAMPLE_BAD)==CONTROLLER_FAULT); assert(controller_transition(CONTROLLER_FAULT,EVENT_RESET)==CONTROLLER_IDLE); assert(controller_transition((enum controller_state)99,EVENT_RESET)==CONTROLLER_FAULT);
```

## Expected failure behavior

Return the named failure or safe-state enumerator for rejected work; never invent an out-of-range enum result or partially publish output.
