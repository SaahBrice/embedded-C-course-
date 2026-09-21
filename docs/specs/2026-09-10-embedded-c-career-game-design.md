# Embedded C Career Game — Design Specification

Date: 2026-09-10

## 1. Purpose

Build a guided, terminal-based engineering career simulation that teaches C programming from its foundations through professional embedded development and reusable library creation. The experience targets a learner who has used another programming language but is learning C and embedded systems.

The curriculum uses the host computer for rapid, testable exercises and an STM32 Nucleo-C031C6 for selected physical-hardware checkpoints. A sensor and data-logging system is the final campaign project.

## 2. Product principles

- Teach genuine C development rather than hiding the compiler or toolchain.
- Use guided explanations and unrestricted hints and solutions.
- Assess understanding through varied engineering work, not only code completion.
- Unlock the main campaign in order while allowing unlimited replay of completed missions.
- Keep curriculum content modular so levels can be inserted, replaced, or extended.
- Introduce physical hardware only when it adds educational value.
- Keep portable logic independent of board-specific implementation details.
- Validate the game with a small representative campaign before producing the full curriculum.

## 3. Core experience

The learner begins as a junior firmware engineer and advances through realistic assignments and promotions. A normal session targets 45–60 minutes. Larger release projects may span multiple sessions and must provide safe checkpoints.

A standard mission follows this loop:

1. Present an engineering briefing and explicit acceptance criteria.
2. Teach the required concepts and supporting foundations.
3. Provide an example or guided experiment when appropriate.
4. Ask the learner to predict, write, debug, review, refactor, or design.
5. Compile and run automated checks while preserving raw diagnostics.
6. Offer unrestricted progressive hints and a full explanation or solution.
7. Require the acceptance criteria to pass before unlocking the next main mission.
8. Present a debrief and record completion.

Viewing a solution has no penalty. A mission may require a small transfer exercise—applying the same concept in a different situation—to reinforce active understanding.

## 4. Terminal interface

The repository will expose a `./learn` launcher. Its command model will include:

- `map`: show campaign stages, completed missions, and the next available mission.
- `start`: begin or resume the current mission.
- `status`: show objectives, attempt state, and available support.
- `test`: compile and run the checks without submitting.
- `hint`: reveal hints progressively, with unrestricted access.
- `solution`: show the explanation and reference solution.
- `submit`: run required checks and complete the mission on success.
- `replay <mission>`: create a new attempt for a completed mission.

Commands must produce actionable messages and retain the underlying compiler, linker, test, or flashing evidence.

## 5. Repository architecture

The repository will use these conceptual areas:

```text
game/          Terminal engine and extension interfaces
curriculum/    Chapters, missions, lessons, tests, hints, and solutions
workspace/     Active and replay attempt workspaces
platforms/     Host simulation and STM32 support
progress/      Local progress and attempt records
docs/          Design, learner, authoring, and maintenance documentation
```

The initial engine will use Python's standard library to coordinate files and external tools. All learner programs remain real C programs compiled by a real C compiler.

Original curriculum content is immutable during play. Starting or replaying a mission creates a separate working copy. Replay never overwrites a previous attempt or completed result.

## 6. Mission package model

A mission is a self-contained directory with:

- A manifest containing its stable identifier, display order, version, prerequisites, objectives, activity type, estimated duration, and platform requirements
- An engineering briefing and lesson material
- Starter files when the activity requires them
- Automated checks and acceptance criteria
- Progressive hints, a full explanation, and a reference implementation for coding activities; non-coding activities provide a model answer instead
- A debrief and optional review questions
- A host-simulation or STM32 variant only when the mission teaches hardware-facing behaviour

Stable identifiers are independent of display order. Prerequisites form an explicit dependency graph, but the primary campaign exposes only the next sequential mission. New intermediary missions can be inserted without renaming existing missions or corrupting progress.

Mission versions are stored with completion records. Updating a mission does not silently invalidate an older completion; migrations or an explicit replay recommendation handle meaningful changes.

Ordinary missions are declarative and data-driven. A narrow extension interface may add new activity and checker types. Extensions must have explicit inputs, outputs, timeouts, and error reporting; arbitrary mission-specific execution inside the engine is not the default content mechanism.

## 7. Activity types

The curriculum will combine:

- Programs and modules written from scratch
- Output and execution prediction
- Memory, pointer, and register tracing
- Defect diagnosis and repair
- Behaviour-preserving refactoring
- Code review and trade-off analysis
- Compiler, linker, debugger, and test-output interpretation
- Datasheet and schematic-extract interpretation
- API, header, driver, and library design
- Simulated peripheral work
- Explicit physical-board deployment
- Multi-module release and integration projects

Conceptual questions support reflection but do not depend on exact prose matching. Required completion is based on objective, automatable criteria whenever possible.

## 8. Feedback and failure handling

Failed checks report information in layers:

1. A plain-language summary
2. The original diagnostic evidence
3. A conceptual hint
4. A directed hint
5. A full explanation or reference solution

The runner must distinguish curriculum errors, missing tools, learner compilation failures, test failures, timeouts, and hardware connection or flashing failures. A broken mission or unavailable external tool must not be presented as a learner mistake.

Attempts and progress use safe writes and remain recoverable after interruption. Hardware operations are always explicit; ordinary testing never flashes the board.

## 9. Curriculum

### Stage 1: Orientation and toolchain

Terminal workflow, source files, compilation, linking, warnings, debugging, binary, and hexadecimal.

### Stage 2: C foundations

Types, variables, expressions, control flow, functions, scope, declarations, and program structure.

### Stage 3: Data and memory

Arrays, strings, pointers, stack and static storage, structs, unions, enums, alignment, lifetime, and memory safety.

### Stage 4: Professional C

Headers, translation units, the preprocessor, error handling, assertions, defensive APIs, undefined behaviour, portability, and relevant C standards.

### Stage 5: Embedded foundations

CPU and memory models, fixed-width integers, bits and masks, `const`, `volatile`, memory-mapped registers, basic electronics, schematics, and datasheets.

### Stage 6: Peripheral engineering

GPIO, interrupts, timers, UART, ADC, PWM, SPI, and I2C. Concepts begin in simulation and selected missions continue on the STM32 board.

### Stage 7: Firmware architecture

State machines, event loops, non-blocking timing, ring buffers, callbacks, hardware abstraction, drivers, configuration, and resource constraints.

### Stage 8: Reliability and tooling

Unit and integration tests, debugging, warnings, host sanitizers, static analysis, concurrency hazards, fault investigation, and basic secure-C practices.

### Stage 9: Reusable libraries

API design, encapsulation, documentation, semantic versioning, configuration, portability, test suites, packaging, and consumer examples.

### Stage 10: Advanced embedded development

Startup concepts, linker scripts, memory sections, boot flow, scheduling, real-time concepts, and an RTOS introduction after the bare-metal foundations.

### Stage 11: Final engineering project

Build a tested sensor and data-logging system. It collects and validates measurements, timestamps events, buffers records, exposes communication, and stores or exports data. It runs first in simulation, deploys suitable components to the STM32, and packages reusable components as documented C libraries.

## 10. Host and STM32 strategy

Host missions provide fast compilation, deterministic inputs, detailed tests, sanitizers, and simulated peripherals. Simulations must expose useful state and events rather than merely printing a predetermined success message.

The STM32 track proceeds through:

1. Toolchain and board-connection verification
2. A minimal known-good build and flash
3. GPIO and UART
4. Timers, interrupts, ADC, and supported communication peripherals
5. Reuse of portable modules from host missions
6. Integration of appropriate final-project components

Hardware-facing code sits behind narrow interfaces. Portable algorithms, protocols, buffers, state machines, and libraries remain host-testable. The course teaches register-level reasoning alongside practical vendor facilities so the learner understands abstractions without spending early lessons on incidental startup complexity.

## 11. Assessment

Each mission declares measurable acceptance criteria. Depending on the activity, checks may cover:

- Successful compilation and linking
- Required warning policy
- Behaviour and edge cases
- Public API compatibility
- Memory and undefined-behaviour checks on the host
- Source or binary size constraints when educationally relevant
- Deterministic simulated timing or peripheral interactions
- Explicit hardware observations for board missions

Only required checks gate progression. Optional challenges and review prompts are clearly labelled and do not block the campaign.

## 12. Delivery phases

### Phase 1: Playable foundation

Implement the command interface, discovery, ordered unlocking, attempt isolation, progress, replay, compilation and testing, hints, solutions, debriefs, diagnostics, and exactly five representative introductory missions. The mission set must include prediction, writing from scratch, debugging, testing, and a small integration assignment.

### Phase 2: C foundations campaign

Expand through functions, arrays, strings, pointers, memory, structures, modular programs, and professional C.

### Phase 3: Embedded simulation

Add register models, simulated peripherals, timing, interrupts, drivers, and hardware-abstraction work.

### Phase 4: STM32 track

Add explicit setup and physical-board checkpoints for the Nucleo-C031C6.

### Phase 5: Advanced firmware and Library Forge

Add architecture, reliability, reusable libraries, real-time concepts, and the final sensor/data-logger campaign.

Each phase begins only after the preceding experience is validated. The first implementation plan covers Phase 1 rather than the entire curriculum.

## 13. Verification requirements

Engine tests must cover:

- Mission discovery and manifest validation
- Stable ordering and prerequisites
- Locked and unlocked mission behaviour
- Attempt creation, isolation, replay, and recovery
- Progress persistence and mission-version handling
- Compiler failures, failed tests, timeouts, and missing tools
- Malformed or incomplete mission packages
- Safe handling of explicit hardware commands

A curriculum-validation command must verify that every published mission has consistent metadata, required files, runnable checks, hints, explanations, and a passing reference solution. The initial representative campaign is the acceptance test for the overall learning loop.

## 14. Out of scope for Phase 1

- A graphical or browser interface
- Cloud accounts, online leaderboards, or social features
- Automatic board flashing during ordinary tests
- A complete RTOS course
- The complete multi-stage curriculum
- A general-purpose untrusted plugin runtime
- Support for additional microcontroller families

These exclusions keep the first release small enough to evaluate before expansion.

## 15. Phase 1 success criteria

Phase 1 is successful when a learner can:

1. Launch the terminal game and see the ordered campaign.
2. Start the first available mission in an isolated workspace.
3. Complete five varied guided missions using real C compilation and checks.
4. Receive clear failures, unrestricted hints, explanations, and solutions.
5. Unlock missions only after required checks pass.
6. Replay a completed mission without damaging prior attempts or progress.
7. Resume safely after stopping the program.

It is also successful when an author can add or insert a valid mission package without modifying the central engine, and the validator detects incomplete or inconsistent mission content.
