#!/usr/bin/env python3
"""Create the initial complete curriculum as editable mission packages.

This script refuses to overwrite an existing curriculum. After generation, each
mission directory is independent and can be edited, reordered, or extended by
following docs/AUTHORING.md; the game never needs this generator at runtime.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CURRICULUM = ROOT / "curriculum"


@dataclass(frozen=True)
class MissionDef:
    id: str
    title: str
    stage: int
    activity: str
    concepts: tuple[str, ...]
    assignment: str
    platform: str = "host"


STAGE_NAMES = {
    1: "Orientation and Toolchain",
    2: "C Foundations",
    3: "Data and Memory",
    4: "Professional C",
    5: "Embedded Foundations",
    6: "Peripheral Engineering",
    7: "Firmware Architecture",
    8: "Reliability and Tooling",
    9: "Library Forge",
    10: "Advanced Embedded Development",
    11: "Sensor Data-Logger Capstone",
}


def stage(stage_no: int, rows: list[tuple]) -> list[MissionDef]:
    result = []
    for row in rows:
        mission_id, title, activity, concepts, assignment, *platform = row
        result.append(MissionDef(
            mission_id, title, stage_no, activity, tuple(concepts), assignment,
            platform[0] if platform else "host",
        ))
    return result


MISSIONS = [
    *stage(1, [
        ("first-build", "Build Your First C Program", "write", ["translation", "main", "standard output"], "Implement and compile a small status program, then verify its exact observable output."),
        ("workstation-orientation", "Implement Your First Firmware Function", "write", ["declarations", "definitions", "unsigned status"], "Implement the function declared by a public header while a trusted driver supplies the program entry point."),
        ("compiler-warnings", "Treat Warnings as Defects", "debug", ["diagnostics", "warning flags", "type conversions"], "Repair a program under strict warning flags without suppressing or weakening any diagnostic."),
        ("source-to-program", "Trace Source to Executable", "predict", ["preprocessing", "compilation", "assembly", "linking"], "Predict which build phase owns each artifact and explain where declaration and definition failures appear."),
        ("binary-and-hex", "Decode Binary and Hexadecimal", "trace", ["base conversion", "bit positions", "hex notation"], "Trace several embedded values across binary, hexadecimal, and decimal representations and show your work."),
        ("gdb-first-steps", "Inspect a Running Program", "debug", ["breakpoints", "step", "print", "backtrace"], "Follow a debugger transcript, identify the defective state transition, and implement the corrected result."),
    ]),
    *stage(2, [
        ("integer-types", "Choose Integer Types Deliberately", "design", ["signedness", "range", "integer promotion"], "Select types for realistic sensor fields and justify every range and signedness choice."),
        ("floating-point-tradeoffs", "Measure Floating-Point Trade-offs", "predict", ["representation", "rounding", "fixed point"], "Predict rounding behavior and propose a fixed-point representation for a constrained measurement."),
        ("operators-expressions", "Control Expression Evaluation", "write", ["precedence", "short circuiting", "side effects"], "Implement an expression-oriented status calculation while keeping evaluation order obvious and defined."),
        ("decisions", "Route Fault States", "write", ["if", "switch", "enumerated states"], "Implement readable decision logic that maps measurements and fault states to explicit actions."),
        ("loops", "Process a Sample Window", "write", ["for", "while", "loop invariants"], "Process a bounded sample window, including empty and boundary cases, without indexing outside it."),
        ("functions", "Extract Testable Functions", "refactor", ["parameters", "return values", "single responsibility"], "Split a monolithic calculation into named functions with narrow contracts and unchanged output."),
        ("scope-and-storage", "Reason About Scope and Storage", "trace", ["block scope", "file scope", "static storage"], "Trace name visibility and object lifetime, then choose the narrowest suitable scope for each object."),
        ("input-validation", "Validate External Input", "debug", ["strtol", "end pointers", "range checks"], "Repair command-line parsing so malformed, trailing, negative, and out-of-range inputs are rejected explicitly."),
        ("decomposition", "Decompose a Firmware Ticket", "design", ["contracts", "cohesion", "coupling"], "Turn a telemetry requirement into small functions with inputs, outputs, dependencies, and failure behavior."),
        ("telemetry-cli-release", "Release: Telemetry Converter", "integrate", ["control flow", "functions", "validation", "formatting"], "Build a complete host telemetry converter from a written interface and black-box acceptance checks."),
    ]),
    *stage(3, [
        ("arrays", "Work Safely with Arrays", "write", ["bounds", "element count", "iteration"], "Implement bounded minimum, maximum, and average operations for a fixed sample array."),
        ("strings", "Handle C Strings Explicitly", "debug", ["null terminator", "buffer capacity", "string APIs"], "Repair unsafe string construction and guarantee termination for every destination capacity."),
        ("pointers", "Read Pointer Relationships", "trace", ["address", "dereference", "pointer arithmetic"], "Draw and explain pointer relationships before implementing a checked array traversal."),
        ("pointer-parameters", "Return Results Through Pointers", "write", ["output parameters", "null checks", "const pointers"], "Implement a parsing function with a const input pointer and checked output parameters."),
        ("memory-lifetime", "Prevent Lifetime Defects", "review", ["automatic storage", "static storage", "dangling pointers"], "Review several returned pointers and classify which remain valid, then redesign the unsafe interfaces."),
        ("structs-unions-enums", "Model a Sensor Packet", "write", ["structures", "unions", "enumerations"], "Model tagged sensor payloads without reading an inactive union member."),
        ("alignment-endianness", "Decode Portable Byte Layouts", "trace", ["padding", "alignment", "endianness"], "Decode a byte protocol with shifts rather than struct casts and explain the portability reason."),
        ("dynamic-memory-policy", "Set an Allocation Policy", "design", ["heap fragmentation", "ownership", "bounded storage"], "Compare static pools and dynamic allocation, then specify an ownership policy for a long-running device."),
        ("packet-parser-release", "Release: Binary Packet Parser", "integrate", ["arrays", "pointers", "structures", "bounds checks"], "Build a length-checked packet parser that rejects truncated, oversized, and unknown packet forms."),
    ]),
    *stage(4, [
        ("headers-and-linking", "Separate Interface from Implementation", "write", ["headers", "translation units", "linkage"], "Split a module into a self-contained public header, private implementation, and consumer."),
        ("preprocessor-discipline", "Use the Preprocessor Carefully", "review", ["include guards", "macros", "conditional compilation"], "Review macros for multiple evaluation and precedence hazards, then propose safer alternatives."),
        ("defensive-apis", "Design Defensive APIs", "design", ["preconditions", "postconditions", "invalid arguments"], "Specify and implement an API whose invalid-input behavior is explicit and testable."),
        ("error-models", "Propagate Errors Without Guessing", "write", ["status codes", "out parameters", "error context"], "Implement layered error propagation without collapsing distinct failures into one success-like value."),
        ("undefined-behavior", "Recognize Undefined Behavior", "debug", ["overflow", "invalid shifts", "aliasing", "sequence rules"], "Find and repair undefined operations while preserving the intended calculation."),
        ("portability", "Write Portable C", "refactor", ["implementation-defined behavior", "limits", "feature boundaries"], "Refactor host-assumption-heavy code to use explicit widths, limits, and conversions."),
        ("function-pointers", "Dispatch with Function Pointers", "write", ["callback signatures", "tables", "null callbacks"], "Implement a typed event dispatch table with validation for unknown events and absent handlers."),
        ("modular-library-release", "Release: Portable CRC Module", "project", ["public API", "private state", "tests", "consumer build"], "Deliver a small multi-file CRC module with a clean header, tests, and a separate consumer."),
    ]),
    *stage(5, [
        ("cpu-memory-model", "Map CPU and Memory Responsibilities", "review", ["registers", "address space", "load/store"], "Explain a load-modify-store sequence and distinguish CPU registers from memory-mapped device registers."),
        ("fixed-width-integers", "Use Fixed-Width Integers", "write", ["stdint", "UINT32_C", "format macros"], "Implement a wire-format counter using exact-width types and portable formatting."),
        ("register-masks", "Manipulate Register Bits", "write", ["mask", "shift", "set clear toggle"], "Implement field extraction and update without disturbing unrelated register bits."),
        ("const-and-volatile", "Apply const and volatile Correctly", "review", ["read-only interfaces", "observable side effects", "optimization"], "Classify pointer qualifiers for buffers and registers, explaining what each qualifier does and does not guarantee."),
        ("memory-mapped-io", "Model Memory-Mapped I/O", "simulate", ["volatile access", "register offsets", "read-modify-write"], "Use a host register model to implement explicit read, modify, and write behavior." , "sim"),
        ("electronics-basics", "Connect Firmware to Electronics", "design", ["voltage", "current", "pull resistors", "active levels"], "Choose safe GPIO modes for LED, button, and open-drain signals and justify the electrical assumptions.", "concept"),
        ("datasheet-reading", "Read a Peripheral Datasheet", "datasheet", ["register map", "reset value", "field access"], "Extract offsets, field widths, reset values, and sequencing constraints from a supplied register excerpt.", "concept"),
        ("register-driver-release", "Release: Register-Level GPIO Driver", "project", ["register masks", "volatile", "API boundary"], "Deliver a tested register-level GPIO driver against the host register model.", "sim"),
    ]),
    *stage(6, [
        ("gpio", "Drive Digital I/O", "simulate", ["mode", "input", "output", "active low"], "Implement and test LED and button logic against a deterministic GPIO simulator.", "sim"),
        ("interrupts", "Keep Interrupt Work Bounded", "review", ["ISR", "shared state", "latency"], "Review an interrupt handler, move slow work to foreground code, and define safe shared-state communication.", "sim"),
        ("timers", "Schedule with Hardware Timers", "simulate", ["tick", "compare", "overflow"], "Configure simulated timer events and reason correctly across counter wraparound.", "sim"),
        ("nonblocking-time", "Replace Blocking Delays", "refactor", ["deadlines", "wrap-safe subtraction", "cooperation"], "Refactor delay-based behavior into a non-blocking update function with wrap-safe timing.", "sim"),
        ("uart", "Build a UART Boundary", "simulate", ["baud", "TX/RX", "framing", "buffers"], "Implement buffered UART command handling that copes with partial input and capacity limits.", "sim"),
        ("adc", "Acquire Analog Samples", "simulate", ["resolution", "reference voltage", "scaling"], "Convert deterministic ADC codes into engineering units with documented rounding and range handling.", "sim"),
        ("pwm", "Control Output with PWM", "simulate", ["frequency", "duty cycle", "timer period"], "Map percentage commands to bounded timer compare values without overflow.", "sim"),
        ("spi", "Transact over SPI", "simulate", ["clock polarity", "phase", "chip select", "full duplex"], "Implement a register-read transaction with explicit chip-select and byte-order behavior.", "sim"),
        ("i2c", "Transact over I2C", "simulate", ["address", "start stop", "ACK NACK"], "Implement a sensor register read and classify address, timeout, and NACK failures.", "sim"),
        ("stm32-toolchain-checkpoint", "Prepare the STM32 Toolchain", "hardware", ["ARM compiler", "debug probe", "OpenOCD", "Cube tools"], "Run the read-only doctor, record installed tools, and select a documented build/flash route.", "stm32"),
        ("stm32-board-checkpoint", "Bring Up the Nucleo-C031C6", "hardware", ["board support", "GPIO", "UART", "explicit flash"], "Build the supplied board project, flash it explicitly, and record LED and serial observations.", "stm32"),
        ("peripheral-console-release", "Release: Peripheral Console", "integrate", ["GPIO", "timer", "UART", "ADC"], "Integrate simulated peripherals behind a command console, then identify the STM32 adapter boundary.", "sim"),
    ]),
    *stage(7, [
        ("state-machines", "Model Behavior as States", "write", ["state", "event", "transition", "guard"], "Implement a total transition function for a sensor acquisition state machine."),
        ("event-loops", "Build a Cooperative Event Loop", "write", ["polling", "events", "bounded work"], "Implement an event loop in which every handler returns promptly and timing remains observable."),
        ("ring-buffers", "Implement a Ring Buffer", "write", ["head", "tail", "full empty policy"], "Implement a fixed-capacity byte ring with explicit full and empty results."),
        ("callbacks", "Inject Behavior with Callbacks", "design", ["function pointers", "context pointer", "ownership"], "Design callback signatures that avoid globals and keep context lifetime explicit."),
        ("hal-design", "Define a Hardware Abstraction Boundary", "refactor", ["ports", "adapters", "portable core"], "Separate portable control logic from GPIO, clock, and transport adapters."),
        ("configuration", "Make Configuration Explicit", "design", ["compile-time", "run-time", "validation"], "Choose compile-time or run-time configuration for each constraint and reject inconsistent settings."),
        ("resource-constraints", "Budget Firmware Resources", "review", ["RAM", "flash", "stack", "time"], "Calculate a resource budget and identify which design assumption dominates each limit."),
        ("controller-release", "Release: Portable Sensor Controller", "project", ["state machine", "event loop", "HAL", "ring buffer"], "Integrate the architecture modules into a deterministic, host-tested sensor controller."),
    ]),
    *stage(8, [
        ("unit-testing", "Test C Modules in Isolation", "write", ["test fixture", "assertion", "boundary case"], "Write tests that expose a real defect in a small C module, then repair the module."),
        ("integration-testing", "Test Collaborating Modules", "integrate", ["fakes", "contracts", "failure injection"], "Test the controller with deterministic fake time, sensor, storage, and transport boundaries."),
        ("gdb-debugging", "Diagnose a Firmware Fault with GDB", "debug", ["backtrace", "watchpoint", "memory examine"], "Use a supplied debugger transcript to locate corruption and implement the minimal repair."),
        ("sanitizers", "Use Host Sanitizers", "debug", ["AddressSanitizer", "UndefinedBehaviorSanitizer", "reproduction"], "Reproduce and repair an out-of-bounds and signed-overflow failure under host sanitizers."),
        ("static-analysis", "Act on Static Analysis", "review", ["data flow", "false positive", "warning policy"], "Triage findings by evidence, repair real defects, and document one justified suppression."),
        ("integer-overflow", "Harden Arithmetic", "write", ["checked operations", "saturation", "conversion"], "Implement checked scaling that cannot wrap before its range validation."),
        ("concurrency", "Reason About Shared State", "trace", ["atomicity", "race", "critical section"], "Trace interrupt/foreground interleavings and redesign the communication path around a single owner."),
        ("secure-c", "Validate Untrusted Data", "review", ["length trust boundary", "integer conversion", "fail closed"], "Review a frame decoder and close length, conversion, and partial-update weaknesses."),
        ("incident-response-release", "Incident: Intermittent Logger Reset", "project", ["reproduction", "fault isolation", "regression test"], "Diagnose a realistic intermittent reset from logs, tests, and sanitizer evidence, then add a regression."),
    ]),
    *stage(9, [
        ("api-design", "Design a Stable Library API", "design", ["consumer needs", "opaque types", "error contract"], "Write a minimal public API for a fixed-capacity record queue and justify what remains private."),
        ("encapsulation", "Hide Library Internals", "refactor", ["public header", "private header", "opaque state"], "Move implementation details out of the consumer-visible interface without changing behavior."),
        ("semantic-versioning", "Version an Embedded Library", "review", ["major", "minor", "patch", "compatibility"], "Classify API changes and create a release note with an accurate semantic version decision."),
        ("library-configuration", "Configure Without Forking", "design", ["configuration struct", "feature macro", "defaults"], "Provide validated configuration points while keeping one tested implementation."),
        ("library-documentation", "Document Contracts and Examples", "write", ["preconditions", "ownership", "thread context", "examples"], "Document every public call and produce one minimal consumer example."),
        ("library-testing", "Build a Library Test Matrix", "integrate", ["unit", "consumer", "configuration", "compatibility"], "Create tests across defaults, boundary configurations, invalid calls, and a separate consumer build."),
        ("packaging", "Install and Package a C Library", "project", ["Make", "CMake", "install layout", "export"], "Build, install into a temporary prefix, and consume the library without source-tree-relative includes."),
        ("consumer-integration-release", "Release: Record Queue Library", "project", ["API", "tests", "documentation", "versioning", "packaging"], "Release the complete portable queue library and verify it through independent consumer projects."),
    ]),
    *stage(10, [
        ("startup-code", "Follow MCU Startup", "trace", ["reset handler", "vector table", "C runtime"], "Trace execution from reset through memory initialization to main and identify responsibilities." , "concept"),
        ("linker-scripts", "Read a Linker Script", "datasheet", ["MEMORY", "SECTIONS", "symbols"], "Map code and data sections to flash and RAM and calculate whether the image fits.", "concept"),
        ("memory-sections", "Place Data Deliberately", "design", ["text", "rodata", "data", "bss", "noinit"], "Choose sections for constants, initialized state, zeroed state, and retained diagnostic state.", "concept"),
        ("boot-flow", "Design a Safe Boot Flow", "review", ["reset cause", "initialization order", "safe state"], "Review boot sequencing and ensure outputs enter a safe state before dependent services start.", "concept"),
        ("cooperative-scheduler", "Implement a Tiny Scheduler", "write", ["period", "deadline", "wraparound"], "Implement a fixed-task cooperative scheduler with wrap-safe release checks."),
        ("real-time-analysis", "Analyze Real-Time Schedulability", "trace", ["worst-case execution", "period", "utilization", "latency"], "Calculate timing budgets and identify a deadline miss before choosing a remedy.", "concept"),
        ("rtos-concepts", "Choose When to Use an RTOS", "design", ["task", "queue", "mutex", "priority inversion"], "Design an RTOS-based alternative, identify synchronization needs, and compare it to the event-loop design.", "concept"),
    ]),
    *stage(11, [
        ("capstone-requirements", "Capstone: Define the Product", "design", ["requirements", "acceptance criteria", "constraints"], "Turn the sensor logger brief into testable functional and non-functional requirements."),
        ("capstone-architecture", "Capstone: Partition the System", "design", ["portable core", "ports", "adapters"], "Partition acquisition, validation, buffering, serialization, storage, and transport behind explicit interfaces."),
        ("sensor-interface", "Capstone: Sensor Port", "write", ["sample type", "status", "fake sensor"], "Implement a sensor port with deterministic host fake and distinct unavailable/range failures."),
        ("sample-validation", "Capstone: Validate Samples", "write", ["range", "quality flags", "partial update"], "Validate whole samples before committing them to the logger state."),
        ("timestamp-injection", "Capstone: Inject Time", "refactor", ["clock port", "monotonic time", "test determinism"], "Remove direct clock access and inject a monotonic timestamp provider."),
        ("record-buffer", "Capstone: Buffer Records", "write", ["fixed capacity", "full policy", "ordering"], "Implement a fixed-capacity record ring with a documented reject-new policy."),
        ("record-serialization", "Capstone: Serialize Deterministically", "write", ["wire format", "endianness", "checksum"], "Serialize records byte by byte into a versioned portable wire format."),
        ("storage-interface", "Capstone: Persist Records", "integrate", ["storage port", "partial write", "retry ownership"], "Implement storage orchestration that reports partial and permanent failures without losing ownership."),
        ("transport-retry", "Capstone: Export Reliably", "write", ["transport port", "bounded retry", "backoff"], "Implement bounded retry while distinguishing temporary from permanent transport errors."),
        ("data-logger-integration", "Capstone: Integrate the Logger", "project", ["acquisition", "validation", "buffer", "storage", "transport"], "Integrate the complete host logger and pass nominal plus injected-failure scenarios."),
        ("data-logger-release", "Final Release: Portable Data Logger", "project", ["library", "host demo", "STM32 adapter", "documentation", "version"], "Package, test, document, and release the reusable data-logger core with a clear STM32 adapter path."),
    ]),
]


CODE_ACTIVITIES = {"write", "debug", "refactor", "simulate", "integrate", "project"}


def q(value: str) -> str:
    return json.dumps(value)


def lesson(mission: MissionDef) -> str:
    concepts = ", ".join(mission.concepts)
    return f"""# {mission.title}

## Why this matters

This assignment focuses on **{concepts}**. In embedded work, correctness is not only about producing the expected value once. Code must keep working for boundary inputs, remain understandable during a fault investigation, and make its assumptions visible to the engineer who integrates it with hardware. A desktop program can often be restarted after a surprise; deployed firmware may run unattended for months. That difference is why this mission asks you to reason before changing the implementation.

## Mental model

Treat every C construct in this lesson as part of a contract. Ask what inputs are accepted, which objects may change, how long every object remains alive, and what the caller observes on failure. For this topic, pay special attention to {concepts}. Write ranges and invariants down instead of relying on intuition. The compiler checks syntax and some type relationships, but it does not prove that an index is in range, that a pointer still names a live object, or that a peripheral sequence obeys a datasheet.

An embedded-friendly workflow is: translate the requirement into an observable example; predict the result; compile with strict warnings; run the smallest useful check; inspect the original evidence; and only then generalize. Keep side effects at narrow boundaries. Portable calculations should be ordinary functions that can run on the host. Hardware access should be explicit enough that a reviewer can identify every read and write.

## Engineering details

The central concepts here are {concepts}. Look for the representation behind the names: exact values, object lifetime, buffer capacity, state transitions, or bit positions. Check zero, one, the largest valid value, and the first invalid value. When a conversion occurs, decide whether information can be lost. When state changes, decide who owns that change. When code interacts with a device, separate the portable decision from the register or driver operation.

Use `./learn test` frequently. A failed build is evidence, not a score. Read the first relevant diagnostic, locate the contract it contradicts, and make one coherent correction. Do not remove warning flags, change expected output, or bypass the public interface. Those actions hide the signal that is trying to teach you.

## Your assignment

{mission.assignment}

Before submitting, explain your chosen invariant in a comment or engineering note, exercise a normal case and a boundary case, and confirm that the required command passes from the attempt directory. Then review the full solution even if your implementation passes: compare interfaces, failure behavior, and readability rather than merely comparing lines.
"""


def briefing(mission: MissionDef, number: int) -> str:
    objectives = "\n".join(f"- {item}" for item in mission.concepts[:3])
    return f"""# Engineering Ticket {number:03d}: {mission.title}

You are assigned to the {STAGE_NAMES[mission.stage]} team. A review has identified a focused gap involving {', '.join(mission.concepts)}.

## Objectives

{objectives}
- Produce an artifact that passes the stated automated checks.
- Explain the boundary or invariant that makes the result dependable.

## Assignment

{mission.assignment}

## Acceptance criteria

- Work only inside the attempt workspace shown by `./learn status`.
- Preserve strict compiler flags and supplied test expectations.
- Run `./learn test` and inspect all diagnostics.
- Use `./learn hint` or `./learn solution` freely whenever it helps you learn.
- Submit only after you can explain why the result works at its boundaries.
"""


def c_reference(mission: MissionDef) -> str:
    marker = mission.id.upper().replace("-", "_")
    concept_comment = ", ".join(mission.concepts)
    stage_body = {
        1: """static int mission_result(void) {\n    const unsigned values[] = {1U, 2U, 3U};\n    unsigned total = 0U;\n    for (size_t i = 0U; i < sizeof values / sizeof values[0]; ++i) { total += values[i]; }\n    return total == 6U;\n}""",
        2: """static int checked_sum(const int *values, size_t count, int *out) {\n    if (values == NULL || out == NULL || count == 0U) { return 0; }\n    int total = 0;\n    for (size_t i = 0U; i < count; ++i) { total += values[i]; }\n    *out = total;\n    return 1;\n}\nstatic int mission_result(void) { const int v[] = {2, 4, 6}; int sum = 0; return checked_sum(v, 3U, &sum) && sum == 12; }""",
        3: """struct sample { uint16_t raw; int valid; };\nstatic int mission_result(void) {\n    const struct sample samples[] = {{100U, 1}, {200U, 1}, {999U, 0}};\n    uint32_t total = 0U;\n    for (const struct sample *p = samples; p != samples + 3; ++p) { if (p->valid) { total += p->raw; } }\n    return total == 300U;\n}""",
        4: """enum status { STATUS_OK, STATUS_ARGUMENT };\ntypedef enum status (*operation)(uint32_t, uint32_t *);\nstatic enum status double_value(uint32_t input, uint32_t *out) { if (out == NULL) return STATUS_ARGUMENT; *out = input * 2U; return STATUS_OK; }\nstatic int mission_result(void) { uint32_t value = 0U; operation op = double_value; return op(21U, &value) == STATUS_OK && value == 42U; }""",
        5: """static volatile uint32_t simulated_register;\nstatic int mission_result(void) {\n    const uint32_t mask = UINT32_C(0x3) << 4U;\n    simulated_register = UINT32_C(0xA5A50000);\n    simulated_register = (simulated_register & ~mask) | (UINT32_C(0x2) << 4U);\n    return ((simulated_register & mask) >> 4U) == UINT32_C(2);\n}""",
        6: """struct peripheral { uint32_t state; uint32_t events; };\nstatic int mission_result(void) {\n    struct peripheral device = {0U, 0U};\n    device.state |= UINT32_C(1) << 2U;\n    device.events++;\n    return (device.state & (UINT32_C(1) << 2U)) != 0U && device.events == 1U;\n}""",
        7: """struct ring { uint8_t data[4]; size_t head, tail, count; };\nstatic int push(struct ring *r, uint8_t value) { if (r == NULL || r->count == 4U) return 0; r->data[r->head] = value; r->head = (r->head + 1U) % 4U; r->count++; return 1; }\nstatic int mission_result(void) { struct ring r = {{0U}, 0U, 0U, 0U}; return push(&r, 42U) && r.count == 1U && r.data[0] == 42U; }""",
        8: """static int checked_add_u32(uint32_t a, uint32_t b, uint32_t *out) { if (out == NULL || UINT32_MAX - a < b) return 0; *out = a + b; return 1; }\nstatic int mission_result(void) { uint32_t value = 0U; return checked_add_u32(40U, 2U, &value) && value == 42U && !checked_add_u32(UINT32_MAX, 1U, &value); }""",
        9: """struct queue { uint8_t items[4]; size_t count; };\nstatic int queue_push(struct queue *queue, uint8_t item) { if (queue == NULL || queue->count == 4U) return 0; queue->items[queue->count++] = item; return 1; }\nstatic int mission_result(void) { struct queue queue = {{0U}, 0U}; return queue_push(&queue, 42U) && queue.count == 1U; }""",
        10: """struct task { uint32_t period; uint32_t last; unsigned runs; };\nstatic void release(struct task *task, uint32_t now) { if ((uint32_t)(now - task->last) >= task->period) { task->last = now; task->runs++; } }\nstatic int mission_result(void) { struct task task = {10U, UINT32_MAX - 4U, 0U}; release(&task, 5U); return task.runs == 1U; }""",
        11: """struct sample { int32_t milli_celsius; uint32_t timestamp_ms; };\nstatic int valid(const struct sample *sample) { return sample != NULL && sample->milli_celsius >= -40000 && sample->milli_celsius <= 125000; }\nstatic int mission_result(void) { const struct sample good = {21500, 42U}; const struct sample bad = {200000, 43U}; return valid(&good) && !valid(&bad); }""",
    }[mission.stage]
    return f"""#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

/* Focus: {concept_comment}. */
{stage_body}

int main(void) {{
    const int passed = mission_result();
    printf("{marker}:%s\\n", passed ? "PASS" : "FAIL");
    return passed ? 0 : 1;
}}
"""


def c_starter(mission: MissionDef) -> str:
    marker = mission.id.upper().replace("-", "_")
    return f"""#include <stdio.h>

/*
 * Ticket: {mission.title}
 * Replace this placeholder with a solution that demonstrates:
 * {', '.join(mission.concepts)}.
 */
static int mission_result(void) {{
    return 0; /* Your implementation begins here. */
}}

int main(void) {{
    const int passed = mission_result();
    printf("{marker}:%s\\n", passed ? "PASS" : "FAIL");
    return passed ? 0 : 1;
}}
"""


MAKEFILE = """CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -O0 -g

.PHONY: all test clean
all: program
program: main.c
\t$(CC) $(CFLAGS) main.c -o $@
test: program
\t./program > actual.txt
\tdiff -u expected.txt actual.txt
clean:
\trm -f program actual.txt
"""


def write_mission(mission: MissionDef, number: int, previous: str | None) -> None:
    stage_slug = STAGE_NAMES[mission.stage].lower().replace(" ", "-")
    directory = CURRICULUM / f"{mission.stage:02d}-{stage_slug}" / f"{number:03d}-{mission.id}"
    (directory / "starter").mkdir(parents=True)
    (directory / "reference").mkdir()
    (directory / "hints").mkdir()
    prerequisites = [] if previous is None else [previous]
    objectives = [
        f"Explain {mission.concepts[0]} in an embedded C context",
        f"Apply {mission.concepts[1] if len(mission.concepts) > 1 else mission.concepts[0]} with explicit boundary behavior",
        "Produce and interpret executable engineering evidence",
    ]
    lines = [
        f"id = {q(mission.id)}", f"title = {q(mission.title)}", 'version = "1.0.0"',
        f"order = {number * 10}", f"stage = {mission.stage}", f"activity = {q(mission.activity)}",
        "duration_minutes = 50", f"platform = {q(mission.platform)}",
        f"prerequisites = [{', '.join(q(value) for value in prerequisites)}]",
        f"objectives = [{', '.join(q(value) for value in objectives)}]",
        'starter = "starter"', 'hints = ["hints/01.md", "hints/02.md", "hints/03.md"]', "",
        "[content]", 'briefing = "briefing.md"', 'lesson = "lesson.md"',
        'debrief = "debrief.md"', 'solution = "solution.md"', "",
    ]
    marker = mission.id.upper().replace("-", "_")
    if mission.activity in CODE_ACTIVITIES:
        lines.extend([
            "[[checks]]", 'id = "build-and-behavior"', 'name = "Strict build and behavior checks"',
            'type = "command"', 'argv = ["make", "test"]', "timeout = 20", "required = true", "",
        ])
        expected = f"{marker}:PASS\n"
        for base, source in (("starter", c_starter(mission)), ("reference", c_reference(mission))):
            (directory / base / "main.c").write_text(source, encoding="utf-8")
            (directory / base / "expected.txt").write_text(expected, encoding="utf-8")
            (directory / base / "Makefile").write_text(MAKEFILE, encoding="utf-8")
        solution_artifact = c_reference(mission)
    else:
        token = f"FINAL: {marker}_REASONED"
        lines.extend([
            "[[checks]]", 'id = "engineering-analysis"', 'name = "Completed engineering analysis"',
            'type = "text_regex"', 'path = "answer.md"', f"pattern = {q(token)}", "required = true", "",
        ])
        questions = "\n".join(f"- Explain the role of **{concept}** and one failure it prevents." for concept in mission.concepts)
        (directory / "starter" / "answer.md").write_text(
            f"# {mission.title} — Engineering Analysis\n\n{questions}\n\n## Decision\n\nWrite your conclusion here.\n",
            encoding="utf-8",
        )
        (directory / "reference" / "answer.md").write_text(
            f"# {mission.title} — Model Analysis\n\n{questions}\n\n"
            f"The decision makes representation, ownership, boundaries, and observable failure explicit. "
            f"It checks normal and limiting cases before changing deployed behavior.\n\n{token}\n",
            encoding="utf-8",
        )
        solution_artifact = (directory / "reference" / "answer.md").read_text(encoding="utf-8")

    (directory / "level.toml").write_text("\n".join(lines), encoding="utf-8")
    (directory / "briefing.md").write_text(briefing(mission, number), encoding="utf-8")
    (directory / "lesson.md").write_text(lesson(mission), encoding="utf-8")
    (directory / "debrief.md").write_text(
        f"# Debrief: {mission.title}\n\n"
        f"You practised {', '.join(mission.concepts)}. The durable result is the reasoning habit: state the "
        "contract, test the boundary, preserve the original evidence, and keep hardware effects behind a narrow interface. "
        "Before moving on, describe one defect your checks would catch and one they would not.\n",
        encoding="utf-8",
    )
    (directory / "solution.md").write_text(
        f"# Full solution: {mission.title}\n\n"
        f"A sound solution makes {', '.join(mission.concepts)} explicit and satisfies this assignment:\n\n"
        f"> {mission.assignment}\n\n"
        "Compare the model with your work by checking inputs, outputs, lifetime, ownership, boundary behavior, and failure evidence. "
        "Different code is acceptable when it preserves the same contract.\n\n"
        f"```{'c' if mission.activity in CODE_ACTIVITIES else 'markdown'}\n{solution_artifact}```\n",
        encoding="utf-8",
    )
    hints = [
        f"# Hint 1 — Model\n\nWrite the contract first. For this mission, name the valid range or state involving {mission.concepts[0]}.\n",
        f"# Hint 2 — Boundary\n\nTest zero or empty input, a normal input, and the first invalid input. Inspect how {mission.concepts[-1]} affects the result.\n",
        "# Hint 3 — Concrete route\n\nRead the acceptance check, preserve its flags and expected result, then implement one small function or one reasoned conclusion. Run `./learn test` and address the first relevant diagnostic. The full solution remains available with `./learn solution`.\n",
    ]
    for index, content in enumerate(hints, 1):
        (directory / "hints" / f"{index:02d}.md").write_text(content, encoding="utf-8")


def main() -> int:
    global CURRICULUM
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=CURRICULUM)
    args = parser.parse_args()
    CURRICULUM = args.output.resolve()
    os.environ["LEARN_C_CURRICULUM_ROOT"] = str(CURRICULUM)
    if CURRICULUM.exists():
        raise SystemExit(f"refusing to overwrite existing curriculum: {CURRICULUM}")
    previous = None
    for number, mission in enumerate(MISSIONS, 1):
        write_mission(mission, number, previous)
        previous = mission.id
    from enhance_curriculum import enhance_curriculum
    enhance_curriculum()
    print(f"Created {len(MISSIONS)} missions across {len(STAGE_NAMES)} stages in {CURRICULUM}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
