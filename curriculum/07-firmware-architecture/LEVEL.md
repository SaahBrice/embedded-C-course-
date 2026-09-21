# Level 7: Firmware Architecture

## Main objective

Organize firmware around states, events, bounded queues, callbacks, configuration, and hardware-independent control.

## What you should know before starting

Complete Level 6; this level builds directly on its C contracts and debugging habits.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Release: Portable Sensor Controller**.

## What you will build and learn

- Organize behavior with states, events, callbacks, queues, and validated configuration
- Separate portable policy from hardware access through injected interfaces
- Release a bounded portable sensor controller

## Ordered sublevels

1. **Model Behavior as States** (`state-machines`) — Implement `controller_transition`: `controller_transition` is total: every state/event pair has a deterministic result, and impossible states enter fault rather than guessing.
2. **Build a Cooperative Event Loop** (`event-loops`) — Implement `task_due`: A scheduler can poll this constant-time predicate without blocking; unsigned elapsed time remains valid through counter wrap.
3. **Implement a Ring Buffer** (`ring-buffers`) — Implement `byte_ring_push`, `byte_ring_pop`: Head owns the next write, tail owns the next read, count distinguishes full from empty, and push rejects new data when full.
4. **Inject Behavior with Callbacks** (`callbacks`) — Implement `bool`, `callback_run_once`: A registered callback is checked, invoked exactly once, and receives the caller-owned context unchanged.
5. **Define a Hardware Abstraction Boundary** (`hal-design`) — Implement `bool`, `void`, `controller_step`: Portable policy depends only on injected operations and context; sensor failure drives the output to its documented safe alarm state.
6. **Make Configuration Explicit** (`configuration`) — Implement `controller_config_valid`: Runtime configuration accepts a bounded nonzero period and an ordered inclusive measurement interval.
7. **Budget Firmware Resources** (`resource-constraints`) — Implement `queue_storage_size`: Static queue storage is calculated with an overflow check before a RAM budget accepts it.
8. **Release: Portable Sensor Controller** (`controller-release`) — FINAL BATTLE — Implement `sensor_controller_due`, `sensor_sample_acceptable`, `sensor_controller_update`: The controller release combines wrap-safe scheduling, bounded sample acceptance, and an explicit state update that counts only ready measurements at a due release.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **state, events, and scheduling** is practised in: Model Behavior as States, Build a Cooperative Event Loop, Implement a Ring Buffer, Inject Behavior with Callbacks, Budget Firmware Resources, Release: Portable Sensor Controller
- **dependency injection and configuration** is practised in: Inject Behavior with Callbacks, Define a Hardware Abstraction Boundary, Make Configuration Explicit, Budget Firmware Resources, Release: Portable Sensor Controller
- **bounded state ownership** is practised in: Model Behavior as States, Implement a Ring Buffer, Inject Behavior with Callbacks, Make Configuration Explicit, Budget Firmware Resources, Release: Portable Sensor Controller

## Final battle

**Release: Portable Sensor Controller** is the last required sublevel. It integrates **Model Behavior as States**, **Build a Cooperative Event Loop**, **Make Configuration Explicit**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
