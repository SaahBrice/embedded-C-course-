# Level 10: Advanced Embedded Development

## Main objective

Reason about startup, linking, memory placement, boot safety, scheduling, deadlines, and appropriate RTOS use.

## What you should know before starting

Complete Level 9; this level builds directly on its C contracts and debugging habits.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Choose When to Use an RTOS**.

## What you will build and learn

- Trace startup and linker responsibilities from reset through main
- Place memory deliberately and schedule bounded work against deadlines
- Choose a cooperative design or RTOS from measured constraints

## Ordered sublevels

1. **Follow MCU Startup** (`startup-code`) — Implement `zero_bss_words`: Startup zeroes exactly the BSS word range and permits an empty range without dereferencing null.
2. **Read a Linker Script** (`linker-scripts`) — Implement `region_contains`: A section fits only when its complete address range lies within a linker memory region without overflow.
3. **Place Data Deliberately** (`memory-sections`) — Implement `choose_object_section`: Mutability, initializer value, and reset retention select the intended object section.
4. **Design a Safe Boot Flow** (`boot-flow`) — Implement `boot_next`: Successful boot advances one ordered phase; any failure or invalid continuation returns outputs to the safe phase.
5. **Implement a Tiny Scheduler** (`cooperative-scheduler`) — Implement `scheduler_release`: One call releases at most one job, advances from the planned deadline to avoid drift, and compares deadlines across wrap.
6. **Analyze Real-Time Schedulability** (`real-time-analysis`) — Implement `nonpreemptive_deadline_met`: Worst-case execution plus blocking must fit the period, using subtraction to avoid overflow.
7. **Choose When to Use an RTOS** (`rtos-concepts`) — FINAL BATTLE — Implement `startup_services_ready`, `queue_absorbs_burst`, `periodic_load_fits`, `rtos_partition_justified`: The architecture battle gates scheduler startup on ready memory and drivers, checks queue burst capacity and execution-plus-blocking deadlines, then decides whether separate RTOS tasks justify their complexity.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **startup, linking, and memory layout** is practised in: Follow MCU Startup, Read a Linker Script, Place Data Deliberately, Design a Safe Boot Flow, Analyze Real-Time Schedulability
- **bounded scheduling and deadlines** is practised in: Follow MCU Startup, Design a Safe Boot Flow, Implement a Tiny Scheduler, Analyze Real-Time Schedulability, Choose When to Use an RTOS
- **firmware architecture tradeoffs** is practised in: Read a Linker Script, Place Data Deliberately, Design a Safe Boot Flow, Implement a Tiny Scheduler, Analyze Real-Time Schedulability, Choose When to Use an RTOS

## Final battle

**Choose When to Use an RTOS** is the last required sublevel. It integrates **Design a Safe Boot Flow**, **Implement a Tiny Scheduler**, **Analyze Real-Time Schedulability**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
