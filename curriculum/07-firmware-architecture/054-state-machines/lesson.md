# Model Behavior as States

## What you are doing

Implement a total transition function for a sensor acquisition state machine. In this version of the exercise you learn by changing and running real C artifacts; there is no reflection or essay to submit.

## Why firmware engineers care

The key ideas are **state, event, transition, guard**. Firmware must keep behaving at boundaries and after unusual inputs, not merely in one demonstration. This exercise turns those ideas into behavior the compiler and tests can observe.

## Files you will edit

Edit `task.c` (keep the public declarations in `task.h` unchanged). Do not edit files below `curriculum/` or the hidden acceptance harness. Your personal copy is inside the attempt workspace printed by `./learn status`.

## Required behavior

`controller_transition` is total: every state/event pair has a deterministic result, and impossible states enter fault rather than guessing.

## Interface you must preserve

```c
enum controller_state { CONTROLLER_IDLE, CONTROLLER_SAMPLING, CONTROLLER_FAULT };
enum controller_event { EVENT_START, EVENT_SAMPLE_OK, EVENT_SAMPLE_BAD, EVENT_RESET };
enum controller_state controller_transition(enum controller_state state, enum controller_event event);
```

## A practical way to begin

1. Read the complete starter and public interface before changing it.
2. Find the placeholder or deliberate defect and predict the first failing case.
3. Make the smallest correct change while keeping strict compiler warnings enabled.
4. Run `./learn test` and address the first useful diagnostic.
5. Check the zero/empty case, an ordinary case, and the first invalid or maximum case.

## Common mistake

Do not weaken the function signature, compiler flags, error result, or bounds just to make one example work. A passing implementation must preserve the contract for callers that you cannot see.

## Success looks like

Implement the declared C interface so every normal, boundary, and invalid case in the immutable harness passes. Run `./learn test`; every required check must report `PASS`. Use `./learn solution` whenever you need the worked implementation—solutions carry no penalty.
