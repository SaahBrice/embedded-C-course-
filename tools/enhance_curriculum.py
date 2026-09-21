#!/usr/bin/env python3
"""Upgrade generated missions to immutable, topic-specific assessments.

The base generator owns ordering and metadata.  This module owns the learning
artifacts and can be run repeatedly after editing mission definitions.
"""

from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import build_curriculum as curriculum_source
from build_curriculum import MISSIONS, MissionDef


STRICT_FLAGS = (
    "-std=c11", "-Wall", "-Wextra", "-Wpedantic", "-Werror", "-O0", "-g",
)

LEVEL_DETAILS = {
    1: ("orientation-toolchain", "Learn how a C source file becomes a running program and use compiler and debugger evidence to repair it."),
    2: ("c-foundations", "Control C values and program flow through deliberate types, expressions, decisions, loops, functions, and validated input."),
    3: ("data-memory", "Work safely with arrays, strings, pointers, object lifetime, structured data, byte layouts, and bounded storage."),
    4: ("professional-c", "Build portable multi-file C modules with defensive interfaces, explicit errors, defined behavior, and typed dispatch."),
    5: ("embedded-foundations", "Connect portable C to CPU memory, exact-width values, register fields, qualifiers, electronics, and datasheets."),
    6: ("peripheral-engineering", "Control and integrate GPIO, time, interrupts, serial buses, analog conversion, and the STM32 board boundary."),
    7: ("firmware-architecture", "Organize firmware around states, events, bounded queues, callbacks, configuration, and hardware-independent control."),
    8: ("reliability-tooling", "Find and prevent defects with tests, debuggers, sanitizers, static analysis, safe arithmetic, concurrency rules, and secure parsing."),
    9: ("library-forge", "Turn embedded C into a documented, versioned, configurable, tested, installable library with private internals."),
    10: ("advanced-embedded", "Reason about startup, linking, memory placement, boot safety, scheduling, deadlines, and appropriate RTOS use."),
    11: ("data-logger-capstone", "Combine the course into a portable, allocation-free sensor data logger with deterministic adapters and failure handling."),
}

LEVEL_OUTCOMES = {
    1: (
        "Compile and run a complete C program with exact output and exit status",
        "Read strict compiler diagnostics and repair type, range, and conversion defects",
        "Use binary, hexadecimal, build-stage, and debugger evidence to locate a defect",
    ),
    2: (
        "Choose C types that match the range and meaning of firmware data",
        "Write decisions, loops, functions, and validated conversions with explicit boundaries",
        "Release a checked telemetry conversion component",
    ),
    3: (
        "Use arrays, strings, pointers, and caller-owned output without crossing object bounds",
        "Reason about lifetime, tagged data, alignment, byte order, and fixed storage",
        "Release a binary packet parser that validates before committing output",
    ),
    4: (
        "Separate declarations and definitions across translation units",
        "Design portable defensive interfaces with meaningful error results and defined behavior",
        "Release a reusable CRC module behind a stable public header",
    ),
    5: (
        "Relate C expressions and qualifiers to CPU, memory, and peripheral-register behavior",
        "Build masks and exact-width operations from electronics and datasheet constraints",
        "Release a register-level GPIO configuration driver",
    ),
    6: (
        "Drive GPIO, time, interrupts, UART, ADC, PWM, SPI, and I2C through deterministic simulations",
        "Keep blocking, ownership, range, and timeout behavior explicit at peripheral boundaries",
        "Build and observe the STM32 path before releasing a peripheral console",
    ),
    7: (
        "Organize behavior with states, events, callbacks, queues, and validated configuration",
        "Separate portable policy from hardware access through injected interfaces",
        "Release a bounded portable sensor controller",
    ),
    8: (
        "Write tests that expose defects and use debugger, sanitizer, and analyzer evidence",
        "Prevent overflow, races, undefined behavior, and unsafe parsing",
        "Repair an intermittent logger-reset incident from reproducible evidence",
    ),
    9: (
        "Design a documented public API while keeping representation private",
        "Version, configure, test, build, install, and relocate a static C library",
        "Prove a consumer can use the record-queue library without source-tree access",
    ),
    10: (
        "Trace startup and linker responsibilities from reset through main",
        "Place memory deliberately and schedule bounded work against deadlines",
        "Choose a cooperative design or RTOS from measured constraints",
    ),
    11: (
        "Turn requirements into injected sensor, time, storage, and transport interfaces",
        "Validate, buffer, serialize, persist, and retry records without dynamic allocation",
        "Release a portable data logger with deterministic failure-injection tests",
    ),
}

# Deliberate practice clusters: every cluster names five or more distinct
# implementations whose coding work genuinely exercises the shared skill.
TOPIC_PRACTICE = {
    1: {
        "strict diagnostics as defects": ["first-build", "workstation-orientation", "compiler-warnings", "source-to-program", "binary-and-hex", "gdb-first-steps"],
        "source, translation, and linking": ["first-build", "workstation-orientation", "compiler-warnings", "source-to-program", "gdb-first-steps"],
        "representation and debugging evidence": ["workstation-orientation", "compiler-warnings", "source-to-program", "binary-and-hex", "gdb-first-steps"],
    },
    2: {
        "numeric representation and safe arithmetic": ["integer-types", "floating-point-tradeoffs", "operators-expressions", "decisions", "loops", "telemetry-cli-release"],
        "control flow and decomposition": ["operators-expressions", "decisions", "loops", "functions", "decomposition", "telemetry-cli-release"],
        "validated status-returning APIs": ["functions", "scope-and-storage", "input-validation", "decomposition", "telemetry-cli-release"],
    },
    3: {
        "bounded arrays and storage": ["arrays", "strings", "pointers", "pointer-parameters", "dynamic-memory-policy", "packet-parser-release"],
        "pointer lifetime and ownership": ["pointers", "pointer-parameters", "memory-lifetime", "structs-unions-enums", "dynamic-memory-policy", "packet-parser-release"],
        "typed and byte-level representation": ["arrays", "pointer-parameters", "structs-unions-enums", "alignment-endianness", "packet-parser-release"],
    },
    4: {
        "public interfaces and translation units": ["headers-and-linking", "preprocessor-discipline", "defensive-apis", "error-models", "function-pointers", "modular-library-release"],
        "validation, errors, and defined behavior": ["defensive-apis", "error-models", "undefined-behavior", "portability", "modular-library-release"],
        "portable operations and typed dispatch": ["headers-and-linking", "undefined-behavior", "portability", "function-pointers", "modular-library-release"],
    },
    5: {
        "fixed-width register arithmetic": ["cpu-memory-model", "fixed-width-integers", "register-masks", "const-and-volatile", "memory-mapped-io", "datasheet-reading", "register-driver-release"],
        "qualifiers and hardware access": ["cpu-memory-model", "register-masks", "const-and-volatile", "memory-mapped-io", "electronics-basics", "register-driver-release"],
        "datasheet-driven driver design": ["fixed-width-integers", "register-masks", "memory-mapped-io", "electronics-basics", "datasheet-reading", "register-driver-release"],
    },
    6: {
        "digital events, timing, and serial I/O": ["gpio", "interrupts", "timers", "nonblocking-time", "uart", "spi", "i2c", "peripheral-console-release"],
        "range-checked peripheral conversion": ["timers", "nonblocking-time", "adc", "pwm", "spi", "i2c", "peripheral-console-release"],
        "simulation through target integration": ["gpio", "uart", "adc", "spi", "i2c", "stm32-toolchain-checkpoint", "stm32-board-checkpoint", "peripheral-console-release"],
    },
    7: {
        "state, events, and scheduling": ["state-machines", "event-loops", "ring-buffers", "callbacks", "resource-constraints", "controller-release"],
        "dependency injection and configuration": ["callbacks", "hal-design", "configuration", "resource-constraints", "controller-release"],
        "bounded state ownership": ["state-machines", "ring-buffers", "callbacks", "configuration", "resource-constraints", "controller-release"],
    },
    8: {
        "executable defect evidence": ["unit-testing", "integration-testing", "gdb-debugging", "sanitizers", "static-analysis", "incident-response-release"],
        "undefined behavior and data integrity": ["sanitizers", "static-analysis", "integer-overflow", "concurrency", "secure-c", "incident-response-release"],
        "regression and recovery reasoning": ["unit-testing", "integration-testing", "gdb-debugging", "concurrency", "secure-c", "incident-response-release"],
    },
    9: {
        "public API and encapsulation": ["api-design", "encapsulation", "semantic-versioning", "library-configuration", "library-documentation", "consumer-integration-release"],
        "verification and release discipline": ["semantic-versioning", "library-documentation", "library-testing", "packaging", "consumer-integration-release"],
        "build, install, and compatibility": ["library-configuration", "library-documentation", "library-testing", "packaging", "consumer-integration-release"],
    },
    10: {
        "startup, linking, and memory layout": ["startup-code", "linker-scripts", "memory-sections", "boot-flow", "real-time-analysis"],
        "bounded scheduling and deadlines": ["startup-code", "boot-flow", "cooperative-scheduler", "real-time-analysis", "rtos-concepts"],
        "firmware architecture tradeoffs": ["linker-scripts", "memory-sections", "boot-flow", "cooperative-scheduler", "real-time-analysis", "rtos-concepts"],
    },
    11: {
        "requirements and injected ports": ["capstone-requirements", "capstone-architecture", "sensor-interface", "sample-validation", "timestamp-injection", "data-logger-integration", "data-logger-release"],
        "buffering, serialization, and persistence": ["record-buffer", "record-serialization", "storage-interface", "transport-retry", "data-logger-integration", "data-logger-release"],
        "failure handling and integrated release": ["sensor-interface", "sample-validation", "storage-interface", "transport-retry", "data-logger-integration", "data-logger-release"],
    },
}

FINAL_INTEGRATES = {
    1: ["compiler-warnings", "source-to-program", "binary-and-hex"],
    2: ["floating-point-tradeoffs", "decisions", "input-validation"],
    3: ["pointers", "structs-unions-enums", "alignment-endianness"],
    4: ["headers-and-linking", "defensive-apis", "error-models"],
    5: ["register-masks", "memory-mapped-io", "datasheet-reading"],
    6: ["gpio", "uart", "stm32-board-checkpoint"],
    7: ["state-machines", "event-loops", "configuration"],
    8: ["static-analysis", "integer-overflow", "concurrency"],
    9: ["library-documentation", "library-testing", "packaging"],
    10: ["boot-flow", "cooperative-scheduler", "real-time-analysis"],
    11: ["capstone-requirements", "record-serialization", "data-logger-integration"],
}


@dataclass(frozen=True)
class Exercise:
    declarations: str
    implementation: str
    tests: str
    contract: str
    starter: str | None = None
    flags: tuple[str, ...] = STRICT_FLAGS


def exercise(
    declarations: str,
    implementation: str,
    tests: str,
    contract: str,
    *,
    starter: str | None = None,
    flags: tuple[str, ...] = STRICT_FLAGS,
) -> Exercise:
    return Exercise(declarations.strip(), implementation.strip(), tests.strip(), contract, starter, flags)


EXERCISES: dict[str, Exercise] = {
    "first-build": exercise(
        "int firmware_status(unsigned boot_count);",
        "int firmware_status(unsigned boot_count) { return boot_count == 0U ? -1 : 0; }",
        "assert(firmware_status(0U) == -1); assert(firmware_status(1U) == 0); assert(firmware_status(42U) == 0);",
        "`firmware_status` returns zero only after at least one successful boot has been observed.",
    ),
    "compiler-warnings": exercise(
        "bool adc_to_millivolts(uint16_t code, uint16_t reference_mv, uint16_t *out_mv);",
        """bool adc_to_millivolts(uint16_t code, uint16_t reference_mv, uint16_t *out_mv) {
    if (out_mv == NULL || code > UINT16_C(4095) || reference_mv == 0U) return false;
    const uint32_t scaled = (uint32_t)code * reference_mv + UINT32_C(2047);
    *out_mv = (uint16_t)(scaled / UINT32_C(4095));
    return true;
}""",
        """uint16_t mv = 99U; assert(adc_to_millivolts(0U, 3300U, &mv) && mv == 0U);
assert(adc_to_millivolts(4095U, 3300U, &mv) && mv == 3300U);
assert(!adc_to_millivolts(4096U, 3300U, &mv)); assert(!adc_to_millivolts(1U, 0U, &mv));""",
        "The multiplication is widened before it occurs, range errors are reported, and strict warnings remain enabled.",
        starter="""#include "task.h"
bool adc_to_millivolts(uint16_t code, uint16_t reference_mv, uint16_t *out_mv) {
    if (out_mv == NULL) return false;
    *out_mv = code * reference_mv / 4095; /* diagnose the conversion and range defects */
    return true;
}""",
        flags=STRICT_FLAGS + ("-Wconversion", "-Wsign-conversion"),
    ),
    "gdb-first-steps": exercise(
        "bool sample_sum(const int16_t *samples, size_t count, int32_t *out_sum);",
        """bool sample_sum(const int16_t *samples, size_t count, int32_t *out_sum) {
    if (samples == NULL || out_sum == NULL) return false;
    int32_t total = 0; for (size_t i = 0U; i < count; ++i) total += samples[i];
    *out_sum = total; return true;
}""",
        """const int16_t v[] = {10, -3, 7}; int32_t sum = 0;
assert(sample_sum(v, 3U, &sum) && sum == 14); assert(sample_sum(v, 0U, &sum) && sum == 0);
assert(!sample_sum(NULL, 1U, &sum)); assert(!sample_sum(v, 3U, NULL));""",
        "`sample_sum` visits exactly `count` live elements and writes the result only through a valid output pointer.",
        starter="""#include "task.h"
bool sample_sum(const int16_t *samples, size_t count, int32_t *out_sum) {
    if (samples == NULL || out_sum == NULL) return false;
    int32_t total = 0; for (size_t i = 0U; i <= count; ++i) total += samples[i];
    *out_sum = total; return true;
}""",
    ),
    "operators-expressions": exercise(
        "uint32_t status_bits_update(uint32_t status, uint32_t set_mask, uint32_t clear_mask);",
        "uint32_t status_bits_update(uint32_t status, uint32_t set_mask, uint32_t clear_mask) { return (status | set_mask) & ~clear_mask; }",
        "assert(status_bits_update(UINT32_C(0x0a), UINT32_C(0x05), UINT32_C(0x08)) == UINT32_C(0x07)); assert(status_bits_update(UINT32_MAX, 0U, UINT32_MAX) == 0U);",
        "The expression sets requested bits, clears requested bits last, and contains no hidden side effects.",
    ),
    "decisions": exercise(
        "enum measurement_action { ACTION_ACCEPT, ACTION_RETRY, ACTION_SHUTDOWN };\nenum measurement_action classify_measurement(int32_t value, bool sensor_fault);",
        """enum measurement_action classify_measurement(int32_t value, bool sensor_fault) {
    if (sensor_fault) return ACTION_SHUTDOWN;
    if (value < -40000 || value > 125000) return ACTION_RETRY;
    return ACTION_ACCEPT;
}""",
        "assert(classify_measurement(20000, false) == ACTION_ACCEPT); assert(classify_measurement(-40001, false) == ACTION_RETRY); assert(classify_measurement(125001, false) == ACTION_RETRY); assert(classify_measurement(20000, true) == ACTION_SHUTDOWN);",
        "Fault status has priority; otherwise the inclusive sensor range is accepted and out-of-range data is retried.",
    ),
    "loops": exercise(
        "bool sample_average(const int16_t *samples, size_t count, int32_t *out_average);",
        """bool sample_average(const int16_t *samples, size_t count, int32_t *out_average) {
    if (samples == NULL || out_average == NULL || count == 0U) return false;
    int64_t total = 0; for (size_t i = 0U; i < count; ++i) total += samples[i];
    *out_average = (int32_t)(total / (int64_t)count); return true;
}""",
        "const int16_t v[] = {3, 6, 9, 12}; int32_t avg = 0; assert(sample_average(v, 4U, &avg) && avg == 7); assert(!sample_average(v, 0U, &avg)); assert(!sample_average(NULL, 1U, &avg));",
        "The loop invariant is that `total` contains exactly the first `i` samples; an empty window has no average.",
    ),
    "functions": exercise(
        "int32_t clamp_i32(int32_t value, int32_t minimum, int32_t maximum);",
        """int32_t clamp_i32(int32_t value, int32_t minimum, int32_t maximum) {
    if (minimum > maximum) return minimum;
    if (value < minimum) return minimum;
    if (value > maximum) return maximum;
    return value;
}""",
        "assert(clamp_i32(5, 0, 10) == 5); assert(clamp_i32(-1, 0, 10) == 0); assert(clamp_i32(11, 0, 10) == 10); assert(clamp_i32(4, 7, 3) == 7);",
        "`clamp_i32` is a pure, independently testable calculation with explicit behavior for an invalid interval.",
    ),
    "input-validation": exercise(
        "bool parse_u16(const char *text, uint16_t *out_value);",
        """bool parse_u16(const char *text, uint16_t *out_value) {
    if (text == NULL || out_value == NULL || text[0] == '\\0' || text[0] == '-') return false;
    errno = 0; char *end = NULL; const unsigned long parsed = strtoul(text, &end, 10);
    if (errno != 0 || end == text || *end != '\\0' || parsed > UINT16_MAX) return false;
    *out_value = (uint16_t)parsed; return true;
}""",
        "uint16_t value = 9U; assert(parse_u16(\"0\", &value) && value == 0U); assert(parse_u16(\"65535\", &value) && value == 65535U); assert(!parse_u16(\"65536\", &value)); assert(!parse_u16(\"-1\", &value)); assert(!parse_u16(\"12x\", &value)); assert(!parse_u16(\"\", &value));",
        "The parser accepts the complete decimal string only, checks conversion errors and range, and never accepts a negative value.",
    ),
    "telemetry-cli-release": exercise(
        "bool celsius_to_milli(double celsius, int32_t *out_milli_celsius);",
        """bool celsius_to_milli(double celsius, int32_t *out_milli_celsius) {
    if (out_milli_celsius == NULL || celsius < -40.0 || celsius > 125.0) return false;
    const double scaled = celsius * 1000.0;
    *out_milli_celsius = (int32_t)(scaled >= 0.0 ? scaled + 0.5 : scaled - 0.5); return true;
}""",
        "int32_t value = 0; assert(celsius_to_milli(21.125, &value) && value == 21125); assert(celsius_to_milli(-0.0006, &value) && value == -1); assert(!celsius_to_milli(125.1, &value));",
        "The converter validates its physical range, rounds to signed milli-degrees, and reports failure separately from a numeric result.",
    ),
    "arrays": exercise(
        "bool sample_minmax(const int16_t *samples, size_t count, int16_t *out_min, int16_t *out_max);",
        """bool sample_minmax(const int16_t *samples, size_t count, int16_t *out_min, int16_t *out_max) {
    if (samples == NULL || count == 0U || out_min == NULL || out_max == NULL) return false;
    int16_t low = samples[0], high = samples[0];
    for (size_t i = 1U; i < count; ++i) { if (samples[i] < low) low = samples[i]; if (samples[i] > high) high = samples[i]; }
    *out_min = low; *out_max = high; return true;
}""",
        "const int16_t v[] = {7, -2, 19, 4}; int16_t low = 0, high = 0; assert(sample_minmax(v, 4U, &low, &high) && low == -2 && high == 19); assert(sample_minmax(v, 1U, &low, &high) && low == 7 && high == 7); assert(!sample_minmax(v, 0U, &low, &high));",
        "The first live element seeds both extrema, and every later index is proven smaller than `count`.",
    ),
    "strings": exercise(
        "bool buffer_append(char *destination, size_t capacity, const char *suffix);",
        """bool buffer_append(char *destination, size_t capacity, const char *suffix) {
    if (destination == NULL || suffix == NULL || capacity == 0U) return false;
    size_t used = 0U; while (used < capacity && destination[used] != '\\0') ++used;
    if (used == capacity) return false;
    const size_t added = strlen(suffix); if (added >= capacity - used) return false;
    memcpy(destination + used, suffix, added + 1U); return true;
}""",
        """char a[8] = \"AB\"; assert(buffer_append(a, sizeof a, \"CDE\") && strcmp(a, \"ABCDE\") == 0);
char b[5] = \"AB\"; assert(!buffer_append(b, sizeof b, \"CDE\") && strcmp(b, \"AB\") == 0);
char c[1] = {0}; assert(buffer_append(c, sizeof c, \"\") && c[0] == '\\0');
char d[3] = {'A','B','C'}; assert(!buffer_append(d, sizeof d, \"x\"));""",
        "`buffer_append` first proves that the destination is terminated within capacity and commits only when suffix plus terminator fits.",
        starter="""#include "task.h"
bool buffer_append(char *destination, size_t capacity, const char *suffix) {
    (void)capacity; strcat(destination, suffix); return true; /* unsafe: repair this boundary */
}""",
    ),
    "pointers": exercise(
        "bool checked_sum(const int32_t *values, size_t count, int64_t *out_sum);",
        """bool checked_sum(const int32_t *values, size_t count, int64_t *out_sum) {
    if (out_sum == NULL || (values == NULL && count != 0U)) return false;
    if (count > SIZE_MAX / sizeof *values) return false;
    int64_t sum = 0; for (size_t index = 0U; index < count; ++index) sum += values[index];
    *out_sum = sum; return true;
}""",
        "const int32_t v[] = {4, 5, 6}; int64_t sum = -1; assert(checked_sum(v, 3U, &sum) && sum == 15); assert(checked_sum(NULL, 0U, &sum) && sum == 0); assert(!checked_sum(NULL, 1U, &sum)); assert(!checked_sum(v, SIZE_MAX, &sum)); assert(!checked_sum(v, 3U, NULL));",
        "A pointer and element count share one provenance-safe contract: null is accepted only for zero elements, impossible byte extents are rejected, and iteration never compares unrelated pointers.",
    ),
    "pointer-parameters": exercise(
        "bool decode_u16_le(const uint8_t *bytes, size_t length, uint16_t *out_value);",
        """bool decode_u16_le(const uint8_t *bytes, size_t length, uint16_t *out_value) {
    if (bytes == NULL || out_value == NULL || length < 2U) return false;
    *out_value = (uint16_t)((uint16_t)bytes[0] | ((uint16_t)bytes[1] << 8U)); return true;
}""",
        "const uint8_t bytes[] = {0x34U, 0x12U}; uint16_t value = 0U; assert(decode_u16_le(bytes, 2U, &value) && value == UINT16_C(0x1234)); assert(!decode_u16_le(bytes, 1U, &value)); assert(!decode_u16_le(NULL, 2U, &value));",
        "The input bytes are read-only, the caller owns the output object, and no byte is read until length is sufficient.",
    ),
    "structs-unions-enums": exercise(
        """enum packet_kind { PACKET_TEMPERATURE, PACKET_HUMIDITY };
struct sensor_packet { enum packet_kind kind; union { int16_t temperature_centi_c; uint16_t humidity_centi_percent; } payload; };
bool packet_value(const struct sensor_packet *packet, int32_t *out_value);""",
        """bool packet_value(const struct sensor_packet *packet, int32_t *out_value) {
    if (packet == NULL || out_value == NULL) return false;
    switch (packet->kind) { case PACKET_TEMPERATURE: *out_value = packet->payload.temperature_centi_c; return true; case PACKET_HUMIDITY: *out_value = packet->payload.humidity_centi_percent; return true; default: return false; }
}""",
        """struct sensor_packet t = {PACKET_TEMPERATURE, {.temperature_centi_c = -125}}; int32_t value = 0;
assert(packet_value(&t, &value) && value == -125); struct sensor_packet h = {PACKET_HUMIDITY, {.humidity_centi_percent = 4567U}}; assert(packet_value(&h, &value) && value == 4567); t.kind = (enum packet_kind)99; assert(!packet_value(&t, &value));""",
        "The enum is the union tag: code reads only the member selected by a recognized tag and rejects every unknown value.",
    ),
    "packet-parser-release": exercise(
        "struct parsed_packet { uint8_t kind; uint16_t value; };\nbool packet_parse(const uint8_t *bytes, size_t length, struct parsed_packet *out_packet);",
        """bool packet_parse(const uint8_t *bytes, size_t length, struct parsed_packet *out_packet) {
    if (bytes == NULL || out_packet == NULL || length != 4U || bytes[1] != 2U || bytes[0] > 1U) return false;
    struct parsed_packet parsed = {bytes[0], (uint16_t)((uint16_t)bytes[2] | ((uint16_t)bytes[3] << 8U))};
    *out_packet = parsed; return true;
}""",
        """const uint8_t good[] = {1U,2U,0x34U,0x12U}; struct parsed_packet out = {9U,9U}; assert(packet_parse(good,4U,&out) && out.kind == 1U && out.value == UINT16_C(0x1234)); assert(!packet_parse(good,3U,&out)); const uint8_t bad_kind[] = {2U,2U,0U,0U}; assert(!packet_parse(bad_kind,4U,&out));""",
        "The parser validates the complete frame shape before committing a temporary decoded packet to caller-owned output.",
    ),
    "headers-and-linking": exercise(
        "uint8_t crc8_update(uint8_t crc, uint8_t byte);",
        """uint8_t crc8_update(uint8_t crc, uint8_t byte) {
    crc ^= byte; for (unsigned bit = 0U; bit < 8U; ++bit) crc = (uint8_t)((crc & 0x80U) ? (uint8_t)(crc << 1U) ^ 0x07U : (uint8_t)(crc << 1U)); return crc;
}""",
        "assert(crc8_update(0U, 0U) == 0U); assert(crc8_update(0U, UINT8_C(0x31)) == UINT8_C(0x97)); assert(crc8_update(UINT8_C(0x5a), UINT8_C(0xc3)) == UINT8_C(0xc6));",
        "`task.h` is self-contained and exposes one external declaration; the separate immutable harness is its consumer translation unit.",
    ),
    "defensive-apis": exercise(
        "bool bounded_copy(uint8_t *destination, size_t capacity, const uint8_t *source, size_t count);",
        """bool bounded_copy(uint8_t *destination, size_t capacity, const uint8_t *source, size_t count) {
    if ((destination == NULL && count != 0U) || (source == NULL && count != 0U) || count > capacity) return false;
    if (count != 0U) memmove(destination, source, count);
    return true;
}""",
        "uint8_t d[4] = {0U}; const uint8_t s[] = {1U,2U,3U}; assert(bounded_copy(d,4U,s,3U) && d[2] == 3U); assert(!bounded_copy(d,2U,s,3U)); assert(bounded_copy(NULL,0U,NULL,0U));",
        "Null pointers are legal only for a zero-length operation, capacity is checked before the first write, and failure leaves storage untouched.",
    ),
    "error-models": exercise(
        "enum scale_status { SCALE_OK, SCALE_ARGUMENT, SCALE_RANGE };\nenum scale_status sensor_scale(uint16_t raw, uint16_t maximum_raw, int32_t *out_milli);",
        """enum scale_status sensor_scale(uint16_t raw, uint16_t maximum_raw, int32_t *out_milli) {
    if (out_milli == NULL || maximum_raw == 0U) return SCALE_ARGUMENT;
    if (raw > maximum_raw) return SCALE_RANGE;
    *out_milli = (int32_t)(((uint32_t)raw * UINT32_C(1000) + maximum_raw / 2U) / maximum_raw); return SCALE_OK;
}""",
        "int32_t out = -1; assert(sensor_scale(5U,10U,&out) == SCALE_OK && out == 500); assert(sensor_scale(11U,10U,&out) == SCALE_RANGE); assert(sensor_scale(1U,0U,&out) == SCALE_ARGUMENT);",
        "Distinct argument and range statuses propagate meaning; the numeric output is written only on success.",
    ),
    "undefined-behavior": exercise(
        "bool safe_left_shift(uint32_t value, unsigned shift, uint32_t *out_value);",
        """bool safe_left_shift(uint32_t value, unsigned shift, uint32_t *out_value) {
    if (out_value == NULL || shift >= 32U || value > (UINT32_MAX >> shift)) return false;
    *out_value = value << shift; return true;
}""",
        "uint32_t out = 0U; assert(safe_left_shift(3U,4U,&out) && out == 48U); assert(!safe_left_shift(1U,32U,&out)); assert(!safe_left_shift(UINT32_MAX,1U,&out));",
        "The shift count is narrower than the type width and the value is proven representable before the shift expression executes.",
        starter="""#include "task.h"
bool safe_left_shift(uint32_t value, unsigned shift, uint32_t *out_value) { *out_value = value << shift; return true; }""",
    ),
    "portability": exercise(
        "bool read_u32_le(const uint8_t *bytes, size_t length, uint32_t *out_value);",
        """bool read_u32_le(const uint8_t *bytes, size_t length, uint32_t *out_value) {
    if (bytes == NULL || out_value == NULL || length < 4U) return false;
    *out_value = (uint32_t)bytes[0] | ((uint32_t)bytes[1] << 8U) | ((uint32_t)bytes[2] << 16U) | ((uint32_t)bytes[3] << 24U); return true;
}""",
        "const uint8_t b[] = {0x78U,0x56U,0x34U,0x12U}; uint32_t out = 0U; assert(read_u32_le(b,4U,&out) && out == UINT32_C(0x12345678)); assert(!read_u32_le(b,3U,&out));",
        "Byte-wise decoding avoids alignment, padding, host-endianness, and aliasing assumptions.",
    ),
    "function-pointers": exercise(
        "typedef bool (*event_handler)(void *context, uint8_t value);\nbool event_dispatch(uint8_t event, event_handler const *handlers, size_t count, void *context, uint8_t value);",
        """bool event_dispatch(uint8_t event, event_handler const *handlers, size_t count, void *context, uint8_t value) {
    if (handlers == NULL || event >= count || handlers[event] == NULL) return false;
    return handlers[event](context, value);
}""",
        """event_handler handlers[] = {capture_handler, NULL}; unsigned total = 0U;
assert(event_dispatch(0U,handlers,2U,&total,7U) && total == 7U); assert(!event_dispatch(1U,handlers,2U,&total,1U)); assert(!event_dispatch(2U,handlers,2U,&total,1U));""",
        "Dispatch validates table bounds and the selected callback before invoking it with the caller-owned context pointer.",
    ),
    "modular-library-release": exercise(
        "uint8_t crc8(const uint8_t *bytes, size_t length);",
        """uint8_t crc8(const uint8_t *bytes, size_t length) {
    if (bytes == NULL && length != 0U) return 0U;
    uint8_t crc = 0U;
    for (size_t i = 0U; i < length; ++i) { crc ^= bytes[i]; for (unsigned bit = 0U; bit < 8U; ++bit) crc = (uint8_t)((crc & 0x80U) ? (uint8_t)(crc << 1U) ^ 0x07U : (uint8_t)(crc << 1U)); } return crc;
}""",
        "const uint8_t data[] = {1U,2U,3U}; assert(crc8(NULL,0U) == 0U); assert(crc8(data,3U) == UINT8_C(0x48)); assert(crc8(data,1U) == UINT8_C(0x07));",
        "A self-contained header plus implementation provides a portable CRC-8/ATM API to an independently compiled consumer.",
    ),
    "fixed-width-integers": exercise(
        "uint32_t saturating_counter_add(uint32_t counter, uint32_t increment);",
        "uint32_t saturating_counter_add(uint32_t counter, uint32_t increment) { return increment > UINT32_MAX - counter ? UINT32_MAX : counter + increment; }",
        "assert(saturating_counter_add(10U,20U) == 30U); assert(saturating_counter_add(UINT32_MAX-1U,2U) == UINT32_MAX); assert(saturating_counter_add(UINT32_MAX,0U) == UINT32_MAX);",
        "The counter has an exact 32-bit representation and saturates instead of wrapping at its maximum wire value.",
    ),
    "register-masks": exercise(
        "bool register_field_write(uint32_t original, uint32_t mask, unsigned shift, uint32_t field_value, uint32_t *out_value);",
        """bool register_field_write(uint32_t original, uint32_t mask, unsigned shift, uint32_t field_value, uint32_t *out_value) {
    if (out_value == NULL || mask == 0U || shift >= 32U || (mask >> shift) == 0U || (field_value & ~(mask >> shift)) != 0U) return false;
    *out_value = (original & ~mask) | ((field_value << shift) & mask); return true;
}""",
        "uint32_t out = 0U; assert(register_field_write(UINT32_C(0xa5a5000f),UINT32_C(0x70),4U,5U,&out)); assert(out == UINT32_C(0xa5a5005f)); assert(!register_field_write(0U,UINT32_C(0x70),4U,8U,&out)); assert(!register_field_write(0U,0U,0U,0U,&out));",
        "The field value is validated against the shifted mask before a clear-and-set update preserves all unrelated bits.",
    ),
    "memory-mapped-io": exercise(
        "bool register_update(volatile uint32_t *reg, uint32_t clear_mask, uint32_t set_mask);",
        """bool register_update(volatile uint32_t *reg, uint32_t clear_mask, uint32_t set_mask) {
    if (reg == NULL) return false;
    const uint32_t current = *reg;
    *reg = (current & ~clear_mask) | set_mask;
    return true;
}""",
        "volatile uint32_t reg = UINT32_C(0xf0); assert(register_update(&reg,UINT32_C(0x30),UINT32_C(0x05)) && reg == UINT32_C(0xc5)); assert(!register_update(NULL,0U,0U));",
        "The volatile register is read once and written once; the pure mask calculation between those observable accesses is explicit.",
    ),
    "register-driver-release": exercise(
        "bool gpio_mode_set(uint32_t original, unsigned pin, uint32_t mode, uint32_t *out_value);",
        """bool gpio_mode_set(uint32_t original, unsigned pin, uint32_t mode, uint32_t *out_value) {
    if (out_value == NULL || pin >= 16U || mode > 3U) return false;
    const unsigned shift = pin * 2U;
    const uint32_t mask = UINT32_C(3) << shift;
    *out_value = (original & ~mask) | (mode << shift);
    return true;
}""",
        "uint32_t out = 0U; assert(gpio_mode_set(UINT32_MAX,5U,1U,&out)); assert(((out >> 10U)&3U)==1U); assert((out & ~(UINT32_C(3)<<10U)) == (UINT32_MAX & ~(UINT32_C(3)<<10U))); assert(!gpio_mode_set(0U,16U,1U,&out));",
        "The driver validates pin and two-bit mode, computes the exact field, and does not disturb any neighboring pin configuration.",
    ),
    "gpio": exercise(
        "bool gpio_output_level(bool command_on, bool active_low);",
        "bool gpio_output_level(bool command_on, bool active_low) { return active_low ? !command_on : command_on; }",
        "assert(gpio_output_level(true,false)); assert(!gpio_output_level(false,false)); assert(!gpio_output_level(true,true)); assert(gpio_output_level(false,true));",
        "Logical device state is converted to an electrical output level in one place, including active-low wiring.",
    ),
    "interrupts": exercise(
        "struct interrupt_mailbox { uint32_t event; bool pending; };\nvoid interrupt_capture(struct interrupt_mailbox *mailbox, uint32_t event);\nbool interrupt_take(struct interrupt_mailbox *mailbox, uint32_t *out_event);",
        """void interrupt_capture(struct interrupt_mailbox *mailbox, uint32_t event) {
    if (mailbox == NULL || mailbox->pending) return;
    mailbox->event = event;
    mailbox->pending = true;
}
bool interrupt_take(struct interrupt_mailbox *mailbox, uint32_t *out_event) {
    if (mailbox == NULL || out_event == NULL || !mailbox->pending) return false;
    *out_event = mailbox->event;
    mailbox->pending = false;
    return true;
}""",
        "struct interrupt_mailbox box={0U,false}; uint32_t event=0U; interrupt_capture(&box,7U); interrupt_capture(&box,9U); assert(interrupt_take(&box,&event)&&event==7U); assert(!interrupt_take(&box,&event)); interrupt_capture(NULL,3U);",
        "The simulated ISR performs one bounded mailbox write and returns; foreground code owns extraction, and a pending event is never silently overwritten.",
    ),
    "timers": exercise(
        "bool deadline_reached(uint32_t now, uint32_t deadline);",
        "bool deadline_reached(uint32_t now, uint32_t deadline) { return (int32_t)(now - deadline) >= 0; }",
        "assert(deadline_reached(100U,100U)); assert(deadline_reached(101U,100U)); assert(!deadline_reached(99U,100U)); assert(deadline_reached(2U,UINT32_MAX-2U));",
        "Signed interpretation of unsigned subtraction gives a wrap-safe deadline decision when intervals remain below half the counter range.",
    ),
    "nonblocking-time": exercise(
        "struct blinker { uint32_t last_change; uint32_t period; bool level; };\nbool blinker_update(struct blinker *blinker, uint32_t now);",
        """bool blinker_update(struct blinker *blinker, uint32_t now) {
    if (blinker == NULL || blinker->period == 0U) return false;
    if ((uint32_t)(now - blinker->last_change) < blinker->period) return false;
    blinker->last_change += blinker->period; blinker->level = !blinker->level; return true;
}""",
        "struct blinker b = {10U,5U,false}; assert(!blinker_update(&b,14U) && !b.level); assert(blinker_update(&b,15U) && b.level && b.last_change == 15U); b.last_change=UINT32_MAX-2U; b.period=5U; assert(blinker_update(&b,2U));",
        "Each call performs bounded work, toggles only after one complete period, and remains correct when the tick counter wraps.",
    ),
    "uart": exercise(
        "#define UART_LINE_CAPACITY 8U\nstruct uart_line { char bytes[UART_LINE_CAPACITY]; size_t length; };\nenum uart_feed_result { UART_MORE, UART_READY, UART_OVERFLOW };\nenum uart_feed_result uart_line_feed(struct uart_line *line, char byte);",
        """enum uart_feed_result uart_line_feed(struct uart_line *line, char byte) {
    if (line == NULL) return UART_OVERFLOW;
    if (byte == '\\n') { line->bytes[line->length] = '\\0'; return UART_READY; }
    if (line->length + 1U >= UART_LINE_CAPACITY) return UART_OVERFLOW;
    line->bytes[line->length++] = byte;
    line->bytes[line->length] = '\\0';
    return UART_MORE;
}""",
        """struct uart_line line = {{0},0U}; assert(uart_line_feed(&line,'O')==UART_MORE); assert(uart_line_feed(&line,'K')==UART_MORE); assert(uart_line_feed(&line,'\\n')==UART_READY); assert(strcmp(line.bytes,\"OK\")==0); struct uart_line full={{0},7U}; assert(uart_line_feed(&full,'x')==UART_OVERFLOW);""",
        "`uart_line_feed` accepts one byte per call, always preserves termination, reports a complete line at newline, and rejects overflow.",
    ),
    "adc": exercise(
        "bool adc_code_to_mv(uint16_t code, uint8_t resolution_bits, uint16_t reference_mv, uint16_t *out_mv);",
        """bool adc_code_to_mv(uint16_t code, uint8_t resolution_bits, uint16_t reference_mv, uint16_t *out_mv) {
    if (out_mv == NULL || resolution_bits == 0U || resolution_bits > 16U || reference_mv == 0U) return false;
    const uint32_t maximum = (UINT32_C(1) << resolution_bits) - 1U;
    if (code > maximum) return false;
    *out_mv = (uint16_t)(((uint32_t)code * reference_mv + maximum / 2U) / maximum);
    return true;
}""",
        "uint16_t mv=0U; assert(adc_code_to_mv(2048U,12U,3300U,&mv) && mv==1650U); assert(adc_code_to_mv(4095U,12U,3300U,&mv) && mv==3300U); assert(!adc_code_to_mv(4096U,12U,3300U,&mv));",
        "Resolution determines the maximum code; widened arithmetic and half-up rounding map only valid codes into millivolts.",
    ),
    "pwm": exercise(
        "bool pwm_compare(uint32_t period_ticks, uint8_t duty_percent, uint32_t *out_compare);",
        """bool pwm_compare(uint32_t period_ticks, uint8_t duty_percent, uint32_t *out_compare) {
    if (out_compare == NULL || period_ticks == 0U || duty_percent > 100U) return false;
    *out_compare = (uint32_t)(((uint64_t)period_ticks * duty_percent + 50U) / 100U);
    return true;
}""",
        "uint32_t compare=0U; assert(pwm_compare(1000U,0U,&compare)&&compare==0U); assert(pwm_compare(1000U,25U,&compare)&&compare==250U); assert(pwm_compare(UINT32_MAX,100U,&compare)&&compare==UINT32_MAX); assert(!pwm_compare(10U,101U,&compare));",
        "Widening prevents multiplication overflow, 0 and 100 percent map to the endpoints, and invalid percentages are rejected.",
    ),
    "spi": exercise(
        "bool spi_build_read(uint8_t register_address, uint8_t *transaction, size_t capacity, size_t *out_length);",
        """bool spi_build_read(uint8_t register_address, uint8_t *transaction, size_t capacity, size_t *out_length) {
    if (transaction == NULL || out_length == NULL || capacity < 2U || register_address > 0x7fU) return false;
    transaction[0] = (uint8_t)(register_address | 0x80U);
    transaction[1] = 0xffU;
    *out_length = 2U;
    return true;
}""",
        "uint8_t tx[2]={0U}; size_t n=0U; assert(spi_build_read(0x12U,tx,2U,&n)&&n==2U&&tx[0]==0x92U&&tx[1]==0xffU); assert(!spi_build_read(0x80U,tx,2U,&n)); assert(!spi_build_read(1U,tx,1U,&n));",
        "The portable transaction builder sets the protocol read bit and dummy byte only after validating address and capacity.",
    ),
    "i2c": exercise(
        "bool i2c_address_byte(uint8_t address_7bit, bool read, uint8_t *out_byte);",
        """bool i2c_address_byte(uint8_t address_7bit, bool read, uint8_t *out_byte) {
    if (out_byte == NULL || address_7bit > 0x7fU) return false;
    *out_byte = (uint8_t)((address_7bit << 1U) | (read ? 1U : 0U));
    return true;
}""",
        "uint8_t byte=0U; assert(i2c_address_byte(0x48U,false,&byte)&&byte==0x90U); assert(i2c_address_byte(0x48U,true,&byte)&&byte==0x91U); assert(!i2c_address_byte(0x80U,true,&byte));",
        "A seven-bit device address and the transfer direction remain separate until the bus address byte is formed.",
    ),
    "peripheral-console-release": exercise(
        "enum console_command { CONSOLE_INVALID, CONSOLE_LED_ON, CONSOLE_LED_OFF, CONSOLE_READ_ADC };\nenum console_command console_parse(const char *line);",
        """enum console_command console_parse(const char *line) {
    if (line == NULL) return CONSOLE_INVALID;
    if (strcmp(line, "LED ON") == 0) return CONSOLE_LED_ON;
    if (strcmp(line, "LED OFF") == 0) return CONSOLE_LED_OFF;
    if (strcmp(line, "READ ADC") == 0) return CONSOLE_READ_ADC;
    return CONSOLE_INVALID;
}""",
        "assert(console_parse(\"LED ON\")==CONSOLE_LED_ON); assert(console_parse(\"LED OFF\")==CONSOLE_LED_OFF); assert(console_parse(\"READ ADC\")==CONSOLE_READ_ADC); assert(console_parse(\"LED\")==CONSOLE_INVALID); assert(console_parse(NULL)==CONSOLE_INVALID);",
        "The console translates complete bounded commands into typed actions and fails closed for partial, unknown, or absent input.",
    ),
    "state-machines": exercise(
        "enum controller_state { CONTROLLER_IDLE, CONTROLLER_SAMPLING, CONTROLLER_FAULT };\nenum controller_event { EVENT_START, EVENT_SAMPLE_OK, EVENT_SAMPLE_BAD, EVENT_RESET };\nenum controller_state controller_transition(enum controller_state state, enum controller_event event);",
        """enum controller_state controller_transition(enum controller_state state, enum controller_event event) {
    switch (state) { case CONTROLLER_IDLE: return event == EVENT_START ? CONTROLLER_SAMPLING : (event == EVENT_RESET ? CONTROLLER_IDLE : CONTROLLER_FAULT); case CONTROLLER_SAMPLING: if (event == EVENT_SAMPLE_OK) return CONTROLLER_IDLE; if (event == EVENT_SAMPLE_BAD) return CONTROLLER_FAULT; return state; case CONTROLLER_FAULT: return event == EVENT_RESET ? CONTROLLER_IDLE : CONTROLLER_FAULT; default: return CONTROLLER_FAULT; }
}""",
        "assert(controller_transition(CONTROLLER_IDLE,EVENT_START)==CONTROLLER_SAMPLING); assert(controller_transition(CONTROLLER_SAMPLING,EVENT_SAMPLE_OK)==CONTROLLER_IDLE); assert(controller_transition(CONTROLLER_SAMPLING,EVENT_SAMPLE_BAD)==CONTROLLER_FAULT); assert(controller_transition(CONTROLLER_FAULT,EVENT_RESET)==CONTROLLER_IDLE); assert(controller_transition((enum controller_state)99,EVENT_RESET)==CONTROLLER_FAULT);",
        "`controller_transition` is total: every state/event pair has a deterministic result, and impossible states enter fault rather than guessing.",
    ),
    "event-loops": exercise(
        "bool task_due(uint32_t now, uint32_t last_run, uint32_t period);",
        "bool task_due(uint32_t now, uint32_t last_run, uint32_t period) { return period != 0U && (uint32_t)(now - last_run) >= period; }",
        "assert(!task_due(14U,10U,5U)); assert(task_due(15U,10U,5U)); assert(task_due(2U,UINT32_MAX-2U,5U)); assert(!task_due(10U,0U,0U));",
        "A scheduler can poll this constant-time predicate without blocking; unsigned elapsed time remains valid through counter wrap.",
    ),
    "ring-buffers": exercise(
        "#define BYTE_RING_CAPACITY 4U\nstruct byte_ring { uint8_t data[BYTE_RING_CAPACITY]; size_t head, tail, count; };\nbool byte_ring_push(struct byte_ring *ring, uint8_t value);\nbool byte_ring_pop(struct byte_ring *ring, uint8_t *out_value);",
        """bool byte_ring_push(struct byte_ring *ring, uint8_t value) { if (ring == NULL || ring->count == BYTE_RING_CAPACITY) return false; ring->data[ring->head] = value; ring->head = (ring->head + 1U) % BYTE_RING_CAPACITY; ++ring->count; return true; }
bool byte_ring_pop(struct byte_ring *ring, uint8_t *out_value) { if (ring == NULL || out_value == NULL || ring->count == 0U) return false; *out_value = ring->data[ring->tail]; ring->tail = (ring->tail + 1U) % BYTE_RING_CAPACITY; --ring->count; return true; }""",
        "struct byte_ring r={{0U},0U,0U,0U}; uint8_t out=0U; assert(!byte_ring_pop(&r,&out)); for(uint8_t i=1U;i<=4U;++i) assert(byte_ring_push(&r,i)); assert(!byte_ring_push(&r,5U)); assert(byte_ring_pop(&r,&out)&&out==1U); assert(byte_ring_push(&r,5U)); for(uint8_t i=2U;i<=5U;++i) assert(byte_ring_pop(&r,&out)&&out==i);",
        "Head owns the next write, tail owns the next read, count distinguishes full from empty, and push rejects new data when full.",
    ),
    "hal-design": exercise(
        "struct controller_hal { void *context; bool (*read_sensor)(void *, int32_t *); void (*set_alarm)(void *, bool); };\nbool controller_step(const struct controller_hal *hal, int32_t maximum);",
        """bool controller_step(const struct controller_hal *hal, int32_t maximum) {
    if (hal == NULL || hal->read_sensor == NULL || hal->set_alarm == NULL) return false;
    int32_t value = 0;
    if (!hal->read_sensor(hal->context, &value)) { hal->set_alarm(hal->context, true); return false; }
    hal->set_alarm(hal->context, value > maximum);
    return true;
}""",
        "struct fake_hal fake={42,false,true}; struct controller_hal hal={&fake,fake_read,fake_alarm}; assert(controller_step(&hal,40)&&fake.alarm); fake.value=10; assert(controller_step(&hal,40)&&!fake.alarm); fake.read_ok=false; assert(!controller_step(&hal,40)&&fake.alarm);",
        "Portable policy depends only on injected operations and context; sensor failure drives the output to its documented safe alarm state.",
    ),
    "controller-release": exercise(
        "struct sensor_controller { uint32_t period; uint32_t last_sample; unsigned samples; };\nbool sensor_controller_update(struct sensor_controller *controller, uint32_t now, bool sensor_ready);",
        """bool sensor_controller_update(struct sensor_controller *controller, uint32_t now, bool sensor_ready) {
    if (controller == NULL || controller->period == 0U || !sensor_ready || (uint32_t)(now-controller->last_sample) < controller->period) return false;
    controller->last_sample += controller->period;
    ++controller->samples;
    return true;
}""",
        "struct sensor_controller c={10U,100U,0U}; assert(!sensor_controller_update(&c,109U,true)); assert(sensor_controller_update(&c,110U,true)&&c.samples==1U&&c.last_sample==110U); assert(!sensor_controller_update(&c,120U,false)&&c.samples==1U);",
        "The integrated controller performs one bounded release at a time, keeps timing state explicit, and never counts an unavailable sample.",
    ),
    "unit-testing": exercise(
        "int16_t median3(int16_t a, int16_t b, int16_t c);",
        """int16_t median3(int16_t a, int16_t b, int16_t c) {
    if (a > b) { const int16_t t=a; a=b; b=t; } if (b > c) { const int16_t t=b; b=c; c=t; } if (a > b) { const int16_t t=a; a=b; b=t; } return b;
}""",
        "assert(median3(1,2,3)==2); assert(median3(3,1,2)==2); assert(median3(2,3,1)==2); assert(median3(-1,-1,7)==-1); assert(median3(INT16_MIN,0,INT16_MAX)==0);",
        "The test matrix covers every ordering class, duplicates, signed values, and representational extremes rather than only the happy path.",
    ),
    "integration-testing": exercise(
        "struct logger_ports { void *context; bool (*read)(void *, int32_t *); bool (*store)(void *, int32_t); };\nbool logger_cycle(const struct logger_ports *ports);",
        """bool logger_cycle(const struct logger_ports *ports) {
    if (ports == NULL || ports->read == NULL || ports->store == NULL) return false;
    int32_t value=0;
    return ports->read(ports->context,&value) && ports->store(ports->context,value);
}""",
        "struct fake_logger f={true,true,42,0,0U,0U}; struct logger_ports p={&f,fake_logger_read,fake_logger_store}; assert(logger_cycle(&p)&&f.stored==42&&f.reads==1U&&f.writes==1U); f.read_ok=false; assert(!logger_cycle(&p)&&f.writes==1U); f.read_ok=true; f.store_ok=false; assert(!logger_cycle(&p));",
        "Deterministic fakes expose call count and transferred value, including read and storage failure branches between collaborating modules.",
    ),
    "gdb-debugging": exercise(
        "size_t replace_value(int32_t *values, size_t count, int32_t target, int32_t replacement);",
        """size_t replace_value(int32_t *values, size_t count, int32_t target, int32_t replacement) {
    if (values == NULL) return 0U;
    size_t changed=0U;
    for(size_t i=0U;i<count;++i) if(values[i]==target){values[i]=replacement;++changed;}
    return changed;
}""",
        "int32_t v[]={1,2,1,3}; assert(replace_value(v,4U,1,9)==2U); assert(v[0]==9&&v[1]==2&&v[2]==9&&v[3]==3); assert(replace_value(v,0U,9,0)==0U); assert(replace_value(NULL,4U,1,2)==0U);",
        "The repaired loop touches exactly the live array range; a watchpoint would show only matching elements being changed.",
    ),
    "sanitizers": exercise(
        "bool copy_samples(int16_t *destination, size_t capacity, const int16_t *source, size_t count);",
        """bool copy_samples(int16_t *destination, size_t capacity, const int16_t *source, size_t count) {
    if ((destination == NULL || source == NULL) && count != 0U) return false;
    if (count > capacity) return false;
    if (count != 0U) memmove(destination,source,count*sizeof *source);
    return true;
}""",
        "int16_t d[3]={0}; const int16_t s[]={1,2,3,4}; assert(copy_samples(d,3U,s,3U)&&d[2]==3); assert(!copy_samples(d,3U,s,4U)); assert(copy_samples(NULL,0U,NULL,0U));",
        "The sanitizer-backed build verifies that byte count derives from a validated element count and no zero-length call dereferences null.",
        starter="""#include "task.h"
bool copy_samples(int16_t *destination, size_t capacity, const int16_t *source, size_t count) { (void)capacity; for(size_t i=0U;i<=count;++i) destination[i]=source[i]; return true; }""",
        flags=STRICT_FLAGS + ("-fsanitize=address,undefined", "-fno-omit-frame-pointer"),
    ),
    "integer-overflow": exercise(
        "bool checked_scale(int32_t value, int32_t multiplier, int32_t *out_value);",
        """bool checked_scale(int32_t value, int32_t multiplier, int32_t *out_value) {
    if (out_value == NULL) return false;
    const int64_t wide=(int64_t)value*multiplier;
    if(wide<INT32_MIN||wide>INT32_MAX)return false;
    *out_value=(int32_t)wide;
    return true;
}""",
        "int32_t out=0; assert(checked_scale(1000,2000,&out)&&out==2000000); assert(checked_scale(-7,6,&out)&&out==-42); assert(!checked_scale(INT32_MAX,2,&out)); assert(!checked_scale(INT32_MIN,-1,&out));",
        "`checked_scale` performs multiplication in a wider defined type and narrows only after both signed limits are proven.",
    ),
    "incident-response-release": exercise(
        "bool watchdog_elapsed(uint32_t now, uint32_t last_kick, uint32_t timeout);",
        "bool watchdog_elapsed(uint32_t now, uint32_t last_kick, uint32_t timeout) { return timeout != 0U && (uint32_t)(now-last_kick) >= timeout; }",
        "assert(!watchdog_elapsed(109U,100U,10U)); assert(watchdog_elapsed(110U,100U,10U)); assert(watchdog_elapsed(3U,UINT32_MAX-5U,8U)); assert(!watchdog_elapsed(10U,0U,0U));",
        "The regression captures the intermittent wraparound reset: elapsed unsigned time, not raw timestamp ordering, determines expiry.",
    ),
    "encapsulation": exercise(
        "typedef struct record_queue record_queue_t;\nsize_t record_queue_required_bytes(void);\nbool record_queue_init(void *storage, size_t storage_size, record_queue_t **out_queue);\nbool record_queue_push(record_queue_t *queue, uint8_t value);\nbool record_queue_pop(record_queue_t *queue, uint8_t *out_value);",
        """struct record_queue { uint8_t data[4]; size_t head,tail,count; };
size_t record_queue_required_bytes(void){return sizeof(struct record_queue);} bool record_queue_init(void *storage,size_t storage_size,record_queue_t **out_queue){if(storage==NULL||out_queue==NULL||storage_size<sizeof(struct record_queue))return false; struct record_queue *q=storage; memset(q,0,sizeof *q); *out_queue=q; return true;} bool record_queue_push(record_queue_t *q,uint8_t value){if(q==NULL||q->count==4U)return false;q->data[q->head]=value;q->head=(q->head+1U)%4U;++q->count;return true;} bool record_queue_pop(record_queue_t *q,uint8_t *out){if(q==NULL||out==NULL||q->count==0U)return false;*out=q->data[q->tail];q->tail=(q->tail+1U)%4U;--q->count;return true;}""",
        "unsigned char storage[128]; record_queue_t *q=NULL; assert(record_queue_required_bytes()<=sizeof storage); assert(record_queue_init(storage,sizeof storage,&q)); uint8_t out=0U; assert(record_queue_push(q,42U)); assert(record_queue_pop(q,&out)&&out==42U); assert(!record_queue_pop(q,&out)); assert(!record_queue_init(storage,1U,&q));",
        "Consumers can name only the opaque queue type; storage sizing and every invariant remain owned by the implementation.",
    ),
    "cooperative-scheduler": exercise(
        "struct scheduled_task { uint32_t period; uint32_t next_release; unsigned runs; };\nbool scheduler_release(struct scheduled_task *task, uint32_t now);",
        """bool scheduler_release(struct scheduled_task *task,uint32_t now){if(task==NULL||task->period==0U||(int32_t)(now-task->next_release)<0)return false;task->next_release+=task->period;++task->runs;return true;}""",
        "struct scheduled_task t={10U,100U,0U}; assert(!scheduler_release(&t,99U)); assert(scheduler_release(&t,100U)&&t.next_release==110U&&t.runs==1U); t.next_release=UINT32_MAX-2U;t.period=5U;assert(scheduler_release(&t,2U));",
        "One call releases at most one job, advances from the planned deadline to avoid drift, and compares deadlines across wrap.",
    ),
    "sensor-interface": exercise(
        "enum sensor_status { SENSOR_OK, SENSOR_UNAVAILABLE, SENSOR_RANGE };\ntypedef enum sensor_status (*sensor_read_fn)(void *context, int32_t *out_value);\nenum sensor_status sensor_read_checked(sensor_read_fn read, void *context, int32_t minimum, int32_t maximum, int32_t *out_value);",
        """enum sensor_status sensor_read_checked(sensor_read_fn read,void *context,int32_t minimum,int32_t maximum,int32_t *out_value){if(read==NULL||out_value==NULL||minimum>maximum)return SENSOR_UNAVAILABLE;int32_t value=0;enum sensor_status status=read(context,&value);if(status!=SENSOR_OK)return status;if(value<minimum||value>maximum)return SENSOR_RANGE;*out_value=value;return SENSOR_OK;}""",
        "struct fake_sensor f={SENSOR_OK,25}; int32_t out=0; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_OK&&out==25); f.value=101; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_RANGE); f.status=SENSOR_UNAVAILABLE; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_UNAVAILABLE);",
        "The sensor port preserves unavailable and range failures as different statuses and commits only a validated reading.",
    ),
    "sample-validation": exercise(
        "struct sensor_sample { int32_t temperature_milli_c; uint16_t humidity_centi_percent; };\nbool sample_valid(const struct sensor_sample *sample);",
        "bool sample_valid(const struct sensor_sample *sample){return sample!=NULL&&sample->temperature_milli_c>=-40000&&sample->temperature_milli_c<=125000&&sample->humidity_centi_percent<=10000U;}",
        "struct sensor_sample s={21000,5000U}; assert(sample_valid(&s)); s.temperature_milli_c=-40001; assert(!sample_valid(&s)); s.temperature_milli_c=0;s.humidity_centi_percent=10001U;assert(!sample_valid(&s));assert(!sample_valid(NULL));",
        "A whole record is accepted only when every field is within its inclusive physical range; no partial state is committed.",
    ),
    "timestamp-injection": exercise(
        "typedef uint32_t (*clock_now_fn)(void *context);\nstruct timestamped_value { uint32_t timestamp_ms; int32_t value; };\nbool timestamp_record(clock_now_fn now, void *context, int32_t value, struct timestamped_value *out_record);",
        "bool timestamp_record(clock_now_fn now,void *context,int32_t value,struct timestamped_value *out_record){if(now==NULL||out_record==NULL)return false;struct timestamped_value record={now(context),value};*out_record=record;return true;}",
        "uint32_t clock=1234U; struct timestamped_value r={0U,0}; assert(timestamp_record(fake_clock,&clock,-7,&r)&&r.timestamp_ms==1234U&&r.value==-7); assert(!timestamp_record(NULL,&clock,1,&r));",
        "Time is injected as a function plus context, making exact timestamps deterministic in tests and independent of a hardware clock.",
    ),
    "record-buffer": exercise(
        "#define RECORD_RING_CAPACITY 3U\nstruct log_record { uint32_t timestamp; int32_t value; };\nstruct record_ring { struct log_record data[RECORD_RING_CAPACITY]; size_t head,tail,count; };\nbool record_ring_push(struct record_ring *ring, struct log_record record);\nbool record_ring_pop(struct record_ring *ring, struct log_record *out_record);",
        "bool record_ring_push(struct record_ring *r,struct log_record v){if(r==NULL||r->count==RECORD_RING_CAPACITY)return false;r->data[r->head]=v;r->head=(r->head+1U)%RECORD_RING_CAPACITY;++r->count;return true;} bool record_ring_pop(struct record_ring *r,struct log_record *out){if(r==NULL||out==NULL||r->count==0U)return false;*out=r->data[r->tail];r->tail=(r->tail+1U)%RECORD_RING_CAPACITY;--r->count;return true;}",
        "struct record_ring q={{{0U,0}},0U,0U,0U}; struct log_record out={0U,0}; for(int32_t i=1;i<=3;++i)assert(record_ring_push(&q,(struct log_record){(uint32_t)i,i}));assert(!record_ring_push(&q,(struct log_record){4U,4}));assert(record_ring_pop(&q,&out)&&out.value==1);assert(record_ring_push(&q,(struct log_record){4U,4}));for(int32_t i=2;i<=4;++i)assert(record_ring_pop(&q,&out)&&out.value==i);",
        "The fixed-capacity ring rejects new records when full and retains FIFO ownership across physical wraparound.",
    ),
    "record-serialization": exercise(
        "#define RECORD_WIRE_SIZE 9U\nstruct serial_record { uint32_t timestamp_ms; int32_t value; };\nbool record_serialize(const struct serial_record *record, uint8_t *bytes, size_t capacity);",
        """bool record_serialize(const struct serial_record *record,uint8_t *bytes,size_t capacity){if(record==NULL||bytes==NULL||capacity<RECORD_WIRE_SIZE)return false;bytes[0]=1U;uint32_t t=record->timestamp_ms;uint32_t v=(uint32_t)record->value;for(unsigned i=0U;i<4U;++i){bytes[1U+i]=(uint8_t)(t>>(8U*i));bytes[5U+i]=(uint8_t)(v>>(8U*i));}return true;}""",
        "struct serial_record r={UINT32_C(0x12345678),-2}; uint8_t b[RECORD_WIRE_SIZE]={0U}; assert(record_serialize(&r,b,sizeof b)); const uint8_t expected[]={1U,0x78U,0x56U,0x34U,0x12U,0xfeU,0xffU,0xffU,0xffU}; assert(memcmp(b,expected,sizeof b)==0); assert(!record_serialize(&r,b,8U));",
        "`record_serialize` emits an explicit version byte and little-endian fields, independent of structure padding and host byte order.",
    ),
    "storage-interface": exercise(
        "typedef size_t (*storage_write_fn)(void *context, const uint8_t *bytes, size_t length);\nbool storage_write_all(storage_write_fn write, void *context, const uint8_t *bytes, size_t length);",
        """bool storage_write_all(storage_write_fn write,void *context,const uint8_t *bytes,size_t length){if(write==NULL||(bytes==NULL&&length!=0U))return false;size_t offset=0U;while(offset<length){size_t n=write(context,bytes+offset,length-offset);if(n==0U||n>length-offset)return false;offset+=n;}return true;}""",
        "const uint8_t data[]={1U,2U,3U,4U,5U}; struct fake_storage s={{0U},0U,2U,false}; assert(storage_write_all(fake_storage_write,&s,data,sizeof data)&&s.length==5U&&memcmp(s.bytes,data,5U)==0); s.length=0U;s.fail=true;assert(!storage_write_all(fake_storage_write,&s,data,sizeof data));",
        "The orchestration retains ownership until every byte is acknowledged, supports valid partial writes, and stops on zero progress.",
    ),
    "transport-retry": exercise(
        "enum transport_status { TRANSPORT_OK, TRANSPORT_TEMPORARY, TRANSPORT_PERMANENT };\ntypedef enum transport_status (*transport_send_fn)(void *context);\nenum transport_status transport_retry(transport_send_fn send, void *context, unsigned max_attempts, unsigned *out_attempts);",
        """enum transport_status transport_retry(transport_send_fn send,void *context,unsigned max_attempts,unsigned *out_attempts){if(send==NULL||out_attempts==NULL||max_attempts==0U)return TRANSPORT_PERMANENT;for(unsigned n=1U;n<=max_attempts;++n){enum transport_status s=send(context);*out_attempts=n;if(s!=TRANSPORT_TEMPORARY)return s;}return TRANSPORT_TEMPORARY;}""",
        "struct fake_transport t={2U,0U,TRANSPORT_OK}; unsigned n=0U; assert(transport_retry(fake_transport_send,&t,4U,&n)==TRANSPORT_OK&&n==3U); t.temporary_left=9U;t.calls=0U;assert(transport_retry(fake_transport_send,&t,2U,&n)==TRANSPORT_TEMPORARY&&n==2U);t.temporary_left=0U;t.final=TRANSPORT_PERMANENT;assert(transport_retry(fake_transport_send,&t,4U,&n)==TRANSPORT_PERMANENT&&n==1U);",
        "Only temporary failures are retried, the bound is exact and observable, and permanent failure returns immediately.",
    ),
    "data-logger-integration": exercise(
        """#define INTEGRATED_LOGGER_CAPACITY 2U
enum logger_io { LOGGER_IO_OK, LOGGER_IO_TEMPORARY, LOGGER_IO_PERMANENT };
enum logger_result { LOGGER_OK, LOGGER_ARGUMENT, LOGGER_SENSOR_FAILURE, LOGGER_RANGE, LOGGER_FULL, LOGGER_EMPTY, LOGGER_STORAGE_FAILURE, LOGGER_TRANSPORT_FAILURE };
struct logger_ports { void *context; enum logger_io (*read)(void *, int32_t *); uint32_t (*now)(void *); enum logger_io (*store)(void *, const uint8_t *, size_t); enum logger_io (*send)(void *, const uint8_t *, size_t); };
struct logger_slot { uint32_t sequence, timestamp; int32_t value; bool persisted; };
struct integrated_logger { struct logger_ports ports; struct logger_slot slots[INTEGRATED_LOGGER_CAPACITY]; size_t head, tail, count; uint32_t next_sequence; unsigned retry_limit; };
enum logger_result logger_init(struct integrated_logger *logger, const struct logger_ports *ports, unsigned retry_limit);
enum logger_result logger_capture(struct integrated_logger *logger);
enum logger_result logger_flush_one(struct integrated_logger *logger);""",
        """static void put_u32(uint8_t *bytes,uint32_t value){for(unsigned i=0U;i<4U;++i)bytes[i]=(uint8_t)(value>>(8U*i));}
enum logger_result logger_init(struct integrated_logger *logger,const struct logger_ports *ports,unsigned retry_limit){
    if(logger==NULL||ports==NULL||ports->read==NULL||ports->now==NULL||ports->store==NULL||ports->send==NULL||retry_limit>3U)return LOGGER_ARGUMENT;
    memset(logger,0,sizeof *logger); logger->ports=*ports; logger->retry_limit=retry_limit; return LOGGER_OK;
}
enum logger_result logger_capture(struct integrated_logger *logger){
    if(logger==NULL)return LOGGER_ARGUMENT;
    if(logger->count==INTEGRATED_LOGGER_CAPACITY)return LOGGER_FULL;
    int32_t value=0; if(logger->ports.read(logger->ports.context,&value)!=LOGGER_IO_OK)return LOGGER_SENSOR_FAILURE;
    if(value < -40000 || value > 125000)return LOGGER_RANGE;
    struct logger_slot slot={logger->next_sequence,logger->ports.now(logger->ports.context),value,false};
    logger->slots[logger->head]=slot; logger->head=(logger->head+1U)%INTEGRATED_LOGGER_CAPACITY; ++logger->count; ++logger->next_sequence; return LOGGER_OK;
}
enum logger_result logger_flush_one(struct integrated_logger *logger){
    if(logger==NULL)return LOGGER_ARGUMENT;
    if(logger->count==0U)return LOGGER_EMPTY;
    struct logger_slot *slot=&logger->slots[logger->tail]; uint8_t wire[12];
    put_u32(wire,slot->sequence); put_u32(wire+4U,slot->timestamp); put_u32(wire+8U,(uint32_t)slot->value);
    if(!slot->persisted){if(logger->ports.store(logger->ports.context,wire,sizeof wire)!=LOGGER_IO_OK)return LOGGER_STORAGE_FAILURE;slot->persisted=true;}
    for(unsigned attempt=0U;attempt<=logger->retry_limit;++attempt){enum logger_io sent=logger->ports.send(logger->ports.context,wire,sizeof wire);if(sent==LOGGER_IO_OK){logger->tail=(logger->tail+1U)%INTEGRATED_LOGGER_CAPACITY;--logger->count;return LOGGER_OK;}if(sent==LOGGER_IO_PERMANENT)return LOGGER_TRANSPORT_FAILURE;}
    return LOGGER_TRANSPORT_FAILURE;
}""",
        """struct integration_fake f={21000,77U,LOGGER_IO_OK,LOGGER_IO_OK,{LOGGER_IO_TEMPORARY,LOGGER_IO_OK},2U,0U,0U,0U};
struct logger_ports ports={&f,integration_read,integration_now,integration_store,integration_send}; struct integrated_logger logger;
assert(logger_init(&logger,&ports,1U)==LOGGER_OK); assert(logger_capture(&logger)==LOGGER_OK&&logger.count==1U&&logger.next_sequence==1U);
assert(logger_flush_one(&logger)==LOGGER_OK&&logger.count==0U&&f.store_calls==1U&&f.send_calls==2U);
f.value=125001; assert(logger_capture(&logger)==LOGGER_RANGE&&logger.count==0U); f.value=42; f.read_result=LOGGER_IO_TEMPORARY; assert(logger_capture(&logger)==LOGGER_SENSOR_FAILURE);
f.read_result=LOGGER_IO_OK; assert(logger_capture(&logger)==LOGGER_OK); f.store_result=LOGGER_IO_TEMPORARY; assert(logger_flush_one(&logger)==LOGGER_STORAGE_FAILURE&&logger.count==1U);""",
        "The integrated logger validates before commit, timestamps and queues accepted samples, persists each record once, retries transport within a bound, and retains ownership after failure.",
    ),
}


# Interrupt work is executable because the shared simulator can deliver a
# deterministic event without real hardware.
EXERCISES["interrupts"] = exercise(
    """struct interrupt_mailbox { uint32_t event; bool pending; };
void interrupt_capture(void *context, uint32_t event);
bool interrupt_take(struct interrupt_mailbox *mailbox, uint32_t *out_event);""",
    """void interrupt_capture(void *context, uint32_t event) {
    struct interrupt_mailbox *mailbox = context;
    if (mailbox == NULL || mailbox->pending) return;
    mailbox->event = event; mailbox->pending = true;
}
bool interrupt_take(struct interrupt_mailbox *mailbox, uint32_t *out_event) {
    if (mailbox == NULL || out_event == NULL || !mailbox->pending) return false;
    *out_event = mailbox->event; mailbox->pending = false; return true;
}""",
    "struct interrupt_mailbox box={0U,false}; uint32_t event=0U; interrupt_capture(&box,7U); assert(interrupt_take(&box,&event)&&event==7U); assert(!interrupt_take(&box,&event));",
    "The interrupt callback performs one bounded mailbox write, never overwrites a pending event, and foreground code explicitly consumes ownership.",
)

# Former prose-only tickets now reinforce a closely related practical C skill.
# The executable contract replaces the essay while each mission retains its own
# firmware context, teaching text, and hints.
PRACTICAL_ALIASES = {
    "workstation-orientation": "first-build",
    "source-to-program": "headers-and-linking",
    "binary-and-hex": "register-masks",
    "integer-types": "fixed-width-integers",
    "floating-point-tradeoffs": "telemetry-cli-release",
    "scope-and-storage": "function-pointers",
    "decomposition": "functions",
    "memory-lifetime": "defensive-apis",
    "alignment-endianness": "portability",
    "dynamic-memory-policy": "ring-buffers",
    "preprocessor-discipline": "register-masks",
    "cpu-memory-model": "memory-mapped-io",
    "const-and-volatile": "memory-mapped-io",
    "electronics-basics": "gpio",
    "datasheet-reading": "register-driver-release",
    "stm32-toolchain-checkpoint": "first-build",
    "callbacks": "function-pointers",
    "configuration": "hal-design",
    "resource-constraints": "ring-buffers",
    "static-analysis": "undefined-behavior",
    "concurrency": "interrupts",
    "secure-c": "packet-parser-release",
    "api-design": "encapsulation",
    "semantic-versioning": "modular-library-release",
    "library-configuration": "hal-design",
    "library-documentation": "headers-and-linking",
    "library-testing": "integration-testing",
    "startup-code": "memory-mapped-io",
    "linker-scripts": "fixed-width-integers",
    "memory-sections": "memory-mapped-io",
    "boot-flow": "state-machines",
    "real-time-analysis": "cooperative-scheduler",
    "rtos-concepts": "event-loops",
    "capstone-requirements": "sample-validation",
    "capstone-architecture": "hal-design",
    "data-logger-release": "data-logger-integration",
}
for practical_id, source_id in PRACTICAL_ALIASES.items():
    EXERCISES[practical_id] = EXERCISES[source_id]

# These topics used to borrow another sublevel's function.  Keep the alias map
# only as historical routing data, but give every published sublevel its own
# coding contract and executable cases.
DISTINCT_ALIAS_EXERCISES: dict[str, Exercise] = {
    "source-to-program": exercise(
        "bool linked_increment(int32_t input, int32_t *out_value);",
        """bool linked_increment(int32_t input, int32_t *out_value) {
    if (out_value == NULL || input == INT32_MAX) return false;
    *out_value = input + 1; return true;
}""",
        "int32_t out=0; assert(linked_increment(0,&out)&&out==1); assert(linked_increment(-2,&out)&&out==-1); assert(!linked_increment(INT32_MAX,&out)); assert(!linked_increment(1,NULL));",
        "A separately declared function produces input plus one, rejects overflow, and writes output only on success.",
    ),
    "binary-and-hex": exercise(
        "uint8_t swap_nibbles(uint8_t value);",
        "uint8_t swap_nibbles(uint8_t value) { return (uint8_t)((value << 4U) | (value >> 4U)); }",
        "assert(swap_nibbles(UINT8_C(0xa5))==UINT8_C(0x5a)); assert(swap_nibbles(UINT8_C(0xf0))==UINT8_C(0x0f)); assert(swap_nibbles(0U)==0U);",
        "The high and low four-bit nibbles exchange positions without changing any bit.",
    ),
    "integer-types": exercise(
        "bool temperature_fits_i16(int32_t milli_celsius);",
        "bool temperature_fits_i16(int32_t milli_celsius) { return milli_celsius >= INT16_MIN && milli_celsius <= INT16_MAX; }",
        "assert(temperature_fits_i16(INT16_MIN)); assert(temperature_fits_i16(INT16_MAX)); assert(!temperature_fits_i16((int32_t)INT16_MIN-1)); assert(!temperature_fits_i16((int32_t)INT16_MAX+1));",
        "The range check proves whether a signed 32-bit measurement can be represented by int16_t before narrowing.",
    ),
    "floating-point-tradeoffs": exercise(
        "bool volts_to_millivolts(double volts, uint32_t *out_millivolts);",
        """bool volts_to_millivolts(double volts, uint32_t *out_millivolts) {
    if (out_millivolts == NULL || volts < 0.0 || volts > 65.535) return false;
    *out_millivolts = (uint32_t)(volts * 1000.0 + 0.5); return true;
}""",
        "uint32_t out=9U; assert(volts_to_millivolts(3.3,&out)&&out==3300U); assert(volts_to_millivolts(0.0006,&out)&&out==1U); assert(!volts_to_millivolts(-0.1,&out)); assert(!volts_to_millivolts(70.0,&out));",
        "Finite nonnegative volts in the documented range are rounded to integer millivolts; invalid ranges are rejected.",
    ),
    "scope-and-storage": exercise(
        "bool instance_increment(unsigned *state);",
        "bool instance_increment(unsigned *state) { if (state == NULL || *state == UINT_MAX) return false; ++*state; return true; }",
        "unsigned a=0U,b=7U; assert(instance_increment(&a)&&a==1U); assert(instance_increment(&b)&&b==8U&&a==1U); a=UINT_MAX; assert(!instance_increment(&a)&&a==UINT_MAX); assert(!instance_increment(NULL));",
        "Caller-owned state keeps independent instances separate and refuses unsigned wraparound.",
    ),
    "decomposition": exercise(
        "bool scale_offset_sample(int32_t raw, int32_t offset, int32_t scale, int32_t *out_value);",
        """bool scale_offset_sample(int32_t raw, int32_t offset, int32_t scale, int32_t *out_value) {
    if (out_value == NULL) return false;
    const int64_t value=((int64_t)raw+offset)*scale;
    if (value<INT32_MIN || value>INT32_MAX) return false;
    *out_value=(int32_t)value; return true;
}""",
        "int32_t out=0; assert(scale_offset_sample(10,-2,3,&out)&&out==24); assert(scale_offset_sample(-5,5,9,&out)&&out==0); assert(!scale_offset_sample(INT32_MAX,1,1,&out)); assert(!scale_offset_sample(1,1,1,NULL));",
        "Parse-free transformation is decomposed into offset, widened scaling, range validation, and one final output commit.",
    ),
    "memory-lifetime": exercise(
        "bool snapshot_i16(const int16_t *source, int16_t *destination);",
        "bool snapshot_i16(const int16_t *source, int16_t *destination) { if (source==NULL||destination==NULL) return false; *destination=*source; return true; }",
        "int16_t source=-7,destination=4; assert(snapshot_i16(&source,&destination)&&destination==-7); source=12; assert(destination==-7); assert(!snapshot_i16(NULL,&destination)); assert(!snapshot_i16(&source,NULL));",
        "The function copies a live value into caller-owned storage instead of returning or retaining a pointer to temporary storage.",
    ),
    "alignment-endianness": exercise(
        "bool decode_u32_be(const uint8_t *bytes, size_t length, uint32_t *out_value);",
        """bool decode_u32_be(const uint8_t *bytes, size_t length, uint32_t *out_value) {
    if (bytes==NULL||out_value==NULL||length<4U) return false;
    *out_value=((uint32_t)bytes[0]<<24U)|((uint32_t)bytes[1]<<16U)|((uint32_t)bytes[2]<<8U)|(uint32_t)bytes[3]; return true;
}""",
        "const uint8_t bytes[]={0x12U,0x34U,0x56U,0x78U}; uint32_t out=0U; assert(decode_u32_be(bytes,4U,&out)&&out==UINT32_C(0x12345678)); assert(!decode_u32_be(bytes,3U,&out)); assert(!decode_u32_be(NULL,4U,&out));",
        "Four protocol bytes are decoded in big-endian order without assuming host alignment or byte order.",
    ),
    "dynamic-memory-policy": exercise(
        "bool fixed_pool_acquire(bool *used, size_t capacity, size_t *out_index);",
        """bool fixed_pool_acquire(bool *used, size_t capacity, size_t *out_index) {
    if (used==NULL||out_index==NULL||capacity==0U) return false;
    for(size_t i=0U;i<capacity;++i) if(!used[i]){used[i]=true;*out_index=i;return true;}
    return false;
}""",
        "bool used[]={true,false,false}; size_t index=99U; assert(fixed_pool_acquire(used,3U,&index)&&index==1U&&used[1]); assert(fixed_pool_acquire(used,3U,&index)&&index==2U); assert(!fixed_pool_acquire(used,3U,&index)); assert(!fixed_pool_acquire(NULL,3U,&index));",
        "A boot-allocated fixed pool returns the first free slot and reports exhaustion without dynamic allocation.",
    ),
    "preprocessor-discipline": exercise(
        "int32_t square_i16_once(int16_t value);",
        "int32_t square_i16_once(int16_t value) { const int32_t widened=value; return widened*widened; }",
        "assert(square_i16_once(0)==0); assert(square_i16_once(-3)==9); assert(square_i16_once(INT16_MAX)==INT32_C(1073676289)); assert(square_i16_once(INT16_MIN)==INT32_C(1073741824));",
        "An inline-style function evaluates its argument once and widens before multiplication, avoiding unsafe square macros.",
    ),
    "cpu-memory-model": exercise(
        "uint32_t load_modify_value(uint32_t loaded, uint32_t set_mask, uint32_t clear_mask);",
        "uint32_t load_modify_value(uint32_t loaded,uint32_t set_mask,uint32_t clear_mask){return (loaded&~clear_mask)|set_mask;}",
        "assert(load_modify_value(UINT32_C(0xf0),UINT32_C(0x05),UINT32_C(0x30))==UINT32_C(0xc5)); assert(load_modify_value(0U,UINT32_C(0x80),0U)==UINT32_C(0x80));",
        "The returned value models the CPU's load-modify phase while preserving bits outside the requested masks.",
    ),
    "const-and-volatile": exercise(
        "bool sample_volatile_register(volatile const uint32_t *reg, uint32_t *out_value);",
        "bool sample_volatile_register(volatile const uint32_t *reg,uint32_t *out_value){if(reg==NULL||out_value==NULL)return false;*out_value=*reg;return true;}",
        "volatile uint32_t reg=UINT32_C(0xa5); uint32_t out=0U; assert(sample_volatile_register(&reg,&out)&&out==UINT32_C(0xa5)); reg=7U; assert(sample_volatile_register(&reg,&out)&&out==7U); assert(!sample_volatile_register(NULL,&out));",
        "The pointer prevents writes through this view while volatile preserves the observable register read.",
    ),
    "electronics-basics": exercise(
        "bool led_output_level(bool active_low, bool led_on);",
        "bool led_output_level(bool active_low,bool led_on){return active_low?!led_on:led_on;}",
        "assert(led_output_level(false,true)); assert(!led_output_level(false,false)); assert(!led_output_level(true,true)); assert(led_output_level(true,false));",
        "The logical LED request is converted to the correct electrical output level for active-high or active-low wiring.",
    ),
    "datasheet-reading": exercise(
        "bool datasheet_field_encode(uint32_t value, unsigned shift, uint32_t mask, uint32_t *out_bits);",
        """bool datasheet_field_encode(uint32_t value,unsigned shift,uint32_t mask,uint32_t *out_bits){
    if(out_bits==NULL||shift>=32U||(mask>>shift)<value)return false;
    *out_bits=(value<<shift)&mask;return true;
}""",
        "uint32_t out=0U; assert(datasheet_field_encode(2U,4U,UINT32_C(0x30),&out)&&out==UINT32_C(0x20)); assert(!datasheet_field_encode(4U,4U,UINT32_C(0x30),&out)); assert(!datasheet_field_encode(1U,32U,UINT32_MAX,&out));",
        "A value is proven to fit a datasheet field before shifting and masking it into register position.",
    ),
    "stm32-toolchain-checkpoint": exercise(
        "bool elf_header_targets_arm(const uint8_t *header, size_t length);",
        "bool elf_header_targets_arm(const uint8_t *header,size_t length){return header!=NULL&&length>=20U&&header[0]==0x7fU&&header[1]=='E'&&header[2]=='L'&&header[3]=='F'&&header[18]==0x28U&&header[19]==0U;}",
        "const uint8_t arm[20]={0x7fU,'E','L','F',0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0x28U,0U}; assert(elf_header_targets_arm(arm,20U)); assert(!elf_header_targets_arm(arm,19U)); uint8_t host[20]={0}; memcpy(host,arm,20U); host[18]=0x3eU; assert(!elf_header_targets_arm(host,20U));",
        "The compiled artifact is accepted only when its ELF magic and machine field identify a little-endian ARM target.",
    ),
    "callbacks": exercise(
        "typedef bool (*status_callback)(void *context, uint8_t value);\nbool callback_run_once(status_callback callback, void *context, uint8_t value);",
        "bool callback_run_once(status_callback callback,void *context,uint8_t value){return callback!=NULL&&callback(context,value);}",
        "unsigned total=1U; assert(callback_run_once(capture_status,&total,4U)&&total==5U); assert(!callback_run_once(NULL,&total,3U)&&total==5U);",
        "A registered callback is checked, invoked exactly once, and receives the caller-owned context unchanged.",
    ),
    "configuration": exercise(
        "bool controller_config_valid(uint32_t sample_period_ms, int32_t low_limit, int32_t high_limit);",
        "bool controller_config_valid(uint32_t sample_period_ms,int32_t low_limit,int32_t high_limit){return sample_period_ms!=0U&&sample_period_ms<=UINT32_C(60000)&&low_limit<=high_limit;}",
        "assert(controller_config_valid(1000U,-40,125)); assert(!controller_config_valid(0U,-40,125)); assert(!controller_config_valid(60001U,-40,125)); assert(!controller_config_valid(10U,5,4));",
        "Runtime configuration accepts a bounded nonzero period and an ordered inclusive measurement interval.",
    ),
    "resource-constraints": exercise(
        "bool queue_storage_size(size_t capacity, size_t item_size, size_t *out_bytes);",
        "bool queue_storage_size(size_t capacity,size_t item_size,size_t *out_bytes){if(out_bytes==NULL||(item_size!=0U&&capacity>SIZE_MAX/item_size))return false;*out_bytes=capacity*item_size;return true;}",
        "size_t out=9U; assert(queue_storage_size(8U,12U,&out)&&out==96U); assert(queue_storage_size(0U,12U,&out)&&out==0U); assert(!queue_storage_size(SIZE_MAX,2U,&out)); assert(!queue_storage_size(1U,1U,NULL));",
        "Static queue storage is calculated with an overflow check before a RAM budget accepts it.",
    ),
    "static-analysis": exercise(
        "bool checked_array_read(const int32_t *values, size_t count, size_t index, int32_t *out_value);",
        "bool checked_array_read(const int32_t *values,size_t count,size_t index,int32_t *out_value){if(values==NULL||out_value==NULL||index>=count)return false;*out_value=values[index];return true;}",
        "const int32_t values[]={4,8,15}; int32_t out=0; assert(checked_array_read(values,3U,2U,&out)&&out==15); assert(!checked_array_read(values,3U,3U,&out)); assert(!checked_array_read(NULL,3U,0U,&out));",
        "Null and bounds findings are repaired with executable checks before the array access occurs.",
    ),
    "concurrency": exercise(
        "bool sequence_is_newer(uint32_t candidate, uint32_t current);",
        "bool sequence_is_newer(uint32_t candidate,uint32_t current){const uint32_t distance=candidate-current;return distance!=0U&&distance<UINT32_C(0x80000000);}",
        "assert(sequence_is_newer(11U,10U)); assert(!sequence_is_newer(10U,10U)); assert(sequence_is_newer(0U,UINT32_MAX)); assert(!sequence_is_newer(UINT32_C(0x80000000),0U));",
        "Single-word sequence snapshots are ordered with defined unsigned wraparound and an explicit half-range rule.",
    ),
    "secure-c": exercise(
        "bool frame_payload_length(const uint8_t *frame, size_t received, size_t *out_length);",
        "bool frame_payload_length(const uint8_t *frame,size_t received,size_t *out_length){if(frame==NULL||out_length==NULL||received<2U)return false;const size_t length=frame[1];if(length>received-2U)return false;*out_length=length;return true;}",
        "const uint8_t good[]={1U,2U,0xaaU,0xbbU}; size_t out=0U; assert(frame_payload_length(good,4U,&out)&&out==2U); const uint8_t bad[]={1U,9U}; assert(!frame_payload_length(bad,2U,&out)); assert(!frame_payload_length(good,1U,&out));",
        "The received extent is validated before trusting an attacker-controlled payload length or publishing it.",
    ),
    "api-design": exercise(
        "bool counter_add_bounded(unsigned current, unsigned increment, unsigned limit, unsigned *out_value);",
        "bool counter_add_bounded(unsigned current,unsigned increment,unsigned limit,unsigned *out_value){if(out_value==NULL||current>limit||increment>limit-current)return false;*out_value=current+increment;return true;}",
        "unsigned out=0U; assert(counter_add_bounded(3U,4U,10U,&out)&&out==7U); assert(counter_add_bounded(10U,0U,10U,&out)&&out==10U); assert(!counter_add_bounded(9U,2U,10U,&out));",
        "The public operation exposes a narrow status-returning contract and never publishes a value beyond its configured limit.",
    ),
    "semantic-versioning": exercise(
        "enum version_change { VERSION_PATCH, VERSION_MINOR, VERSION_MAJOR };\nenum version_change classify_version_change(bool breaks_api, bool adds_api);",
        "enum version_change classify_version_change(bool breaks_api,bool adds_api){if(breaks_api)return VERSION_MAJOR;if(adds_api)return VERSION_MINOR;return VERSION_PATCH;}",
        "assert(classify_version_change(false,false)==VERSION_PATCH); assert(classify_version_change(false,true)==VERSION_MINOR); assert(classify_version_change(true,false)==VERSION_MAJOR); assert(classify_version_change(true,true)==VERSION_MAJOR);",
        "A breaking public change is major, a backward-compatible addition is minor, and an internal fix is patch.",
    ),
    "library-configuration": exercise(
        "bool queue_config_valid(size_t capacity, bool overwrite_oldest);",
        "bool queue_config_valid(size_t capacity,bool overwrite_oldest){(void)overwrite_oldest;return capacity>=2U&&capacity<=1024U&&(capacity&(capacity-1U))==0U;}",
        "assert(queue_config_valid(2U,false)); assert(queue_config_valid(128U,true)); assert(!queue_config_valid(0U,false)); assert(!queue_config_valid(3U,false)); assert(!queue_config_valid(2048U,true));",
        "Queue configuration accepts only supported power-of-two capacities while treating policy as an explicit option.",
    ),
    "library-documentation": exercise(
        "bool documented_copy(uint8_t *destination, size_t capacity, const uint8_t *source, size_t count);",
        "bool documented_copy(uint8_t *destination,size_t capacity,const uint8_t *source,size_t count){if(count>capacity||(count!=0U&&(destination==NULL||source==NULL)))return false;if(count!=0U)memcpy(destination,source,count);return true;}",
        "uint8_t out[3]={0}; const uint8_t in[]={1U,2U,3U}; assert(documented_copy(out,3U,in,3U)&&out[2]==3U); assert(!documented_copy(out,2U,in,3U)); assert(documented_copy(NULL,0U,NULL,0U));",
        "The executable API matches a documentable ownership, nullability, capacity, and zero-length contract.",
    ),
    "library-testing": exercise(
        "bool ring_state_valid(size_t head, size_t tail, size_t count, size_t capacity);",
        "bool ring_state_valid(size_t head,size_t tail,size_t count,size_t capacity){return capacity!=0U&&head<capacity&&tail<capacity&&count<=capacity;}",
        "assert(ring_state_valid(0U,0U,0U,4U)); assert(ring_state_valid(0U,0U,4U,4U)); assert(ring_state_valid(3U,1U,2U,4U)); assert(!ring_state_valid(4U,0U,0U,4U)); assert(!ring_state_valid(0U,0U,1U,0U));",
        "Tests can state and exercise empty, full, wrapped, and invalid ring-buffer invariants independently of implementation.",
    ),
    "startup-code": exercise(
        "bool zero_bss_words(uint32_t *words, size_t count);",
        "bool zero_bss_words(uint32_t *words,size_t count){if(words==NULL&&count!=0U)return false;for(size_t i=0U;i<count;++i)words[i]=0U;return true;}",
        "uint32_t words[]={1U,2U,3U}; assert(zero_bss_words(words,3U)&&words[0]==0U&&words[2]==0U); assert(zero_bss_words(NULL,0U)); assert(!zero_bss_words(NULL,1U));",
        "Startup zeroes exactly the BSS word range and permits an empty range without dereferencing null.",
    ),
    "linker-scripts": exercise(
        "bool region_contains(uint32_t origin, uint32_t length, uint32_t address, uint32_t size);",
        "bool region_contains(uint32_t origin,uint32_t length,uint32_t address,uint32_t size){return length<=UINT32_MAX-origin&&address>=origin&&size<=length&&(address-origin)<=length-size;}",
        "assert(region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x20000000),16U)); assert(region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x200003f0),16U)); assert(!region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x1fffffff),1U)); assert(!region_contains(UINT32_C(0xfffffff0),32U,UINT32_C(0xfffffff0),32U));",
        "A section fits only when its complete address range lies within a linker memory region without overflow.",
    ),
    "memory-sections": exercise(
        "enum object_section { SECTION_RODATA, SECTION_DATA, SECTION_BSS, SECTION_NOINIT };\nenum object_section choose_object_section(bool writable, bool has_nonzero_initializer, bool retain_across_reset);",
        "enum object_section choose_object_section(bool writable,bool has_nonzero_initializer,bool retain_across_reset){if(retain_across_reset)return SECTION_NOINIT;if(!writable)return SECTION_RODATA;return has_nonzero_initializer?SECTION_DATA:SECTION_BSS;}",
        "assert(choose_object_section(false,true,false)==SECTION_RODATA); assert(choose_object_section(true,true,false)==SECTION_DATA); assert(choose_object_section(true,false,false)==SECTION_BSS); assert(choose_object_section(true,false,true)==SECTION_NOINIT);",
        "Mutability, initializer value, and reset retention select the intended object section.",
    ),
    "boot-flow": exercise(
        "enum boot_phase { BOOT_SAFE_OUTPUTS, BOOT_CLOCKS, BOOT_DRIVERS, BOOT_ENABLE_ACTUATORS, BOOT_READY };\nenum boot_phase boot_next(enum boot_phase current, bool step_ok);",
        "enum boot_phase boot_next(enum boot_phase current,bool step_ok){if(!step_ok||current>=BOOT_READY)return BOOT_SAFE_OUTPUTS;return (enum boot_phase)(current+1);}",
        "assert(boot_next(BOOT_SAFE_OUTPUTS,true)==BOOT_CLOCKS); assert(boot_next(BOOT_DRIVERS,true)==BOOT_ENABLE_ACTUATORS); assert(boot_next(BOOT_CLOCKS,false)==BOOT_SAFE_OUTPUTS); assert(boot_next(BOOT_READY,true)==BOOT_SAFE_OUTPUTS);",
        "Successful boot advances one ordered phase; any failure or invalid continuation returns outputs to the safe phase.",
    ),
    "real-time-analysis": exercise(
        "bool nonpreemptive_deadline_met(uint32_t wcet_us, uint32_t blocking_us, uint32_t period_us);",
        "bool nonpreemptive_deadline_met(uint32_t wcet_us,uint32_t blocking_us,uint32_t period_us){return wcet_us<=period_us&&blocking_us<=period_us-wcet_us;}",
        "assert(nonpreemptive_deadline_met(200U,100U,1000U)); assert(nonpreemptive_deadline_met(500U,500U,1000U)); assert(!nonpreemptive_deadline_met(900U,200U,1000U)); assert(!nonpreemptive_deadline_met(1001U,0U,1000U));",
        "Worst-case execution plus blocking must fit the period, using subtraction to avoid overflow.",
    ),
    "rtos-concepts": exercise(
        "bool queue_absorbs_burst(size_t producer_burst, size_t consumer_progress, size_t queue_capacity);",
        "bool queue_absorbs_burst(size_t producer_burst,size_t consumer_progress,size_t queue_capacity){return producer_burst<=consumer_progress||producer_burst-consumer_progress<=queue_capacity;}",
        "assert(queue_absorbs_burst(8U,3U,5U)); assert(queue_absorbs_burst(3U,8U,0U)); assert(!queue_absorbs_burst(9U,3U,5U)); assert(queue_absorbs_burst(SIZE_MAX,SIZE_MAX,0U));",
        "A bounded task queue is sufficient only when it can absorb the producer burst left after consumer progress.",
    ),
    "capstone-requirements": exercise(
        "bool logger_requirements_valid(uint32_t period_ms, uint32_t jitter_ms, size_t record_capacity);",
        "bool logger_requirements_valid(uint32_t period_ms,uint32_t jitter_ms,size_t record_capacity){return period_ms!=0U&&jitter_ms<=period_ms/10U&&record_capacity>=2U&&record_capacity<=1024U;}",
        "assert(logger_requirements_valid(1000U,100U,64U)); assert(!logger_requirements_valid(0U,0U,64U)); assert(!logger_requirements_valid(1000U,101U,64U)); assert(!logger_requirements_valid(1000U,50U,1U));",
        "Logger requirements enforce a nonzero period, at most ten-percent jitter, and a bounded static record capacity.",
    ),
    "capstone-architecture": exercise(
        "bool logger_ports_ready(bool sensor, bool clock, bool storage, bool transport);",
        "bool logger_ports_ready(bool sensor,bool clock,bool storage,bool transport){return sensor&&clock&&storage&&transport;}",
        "assert(logger_ports_ready(true,true,true,true)); assert(!logger_ports_ready(false,true,true,true)); assert(!logger_ports_ready(true,false,true,true)); assert(!logger_ports_ready(true,true,false,true)); assert(!logger_ports_ready(true,true,true,false));",
        "Initialization succeeds only when all four injected hardware boundaries are present.",
    ),
    "data-logger-release": exercise(
        "uint32_t logger_release_checksum(const uint8_t *bytes, size_t length);",
        "uint32_t logger_release_checksum(const uint8_t *bytes,size_t length){uint32_t hash=UINT32_C(2166136261);if(bytes==NULL&&length!=0U)return 0U;for(size_t i=0U;i<length;++i){hash^=bytes[i];hash*=UINT32_C(16777619);}return hash;}",
        "const uint8_t record[]={1U,2U,3U}; assert(logger_release_checksum(record,3U)==UINT32_C(1456420779)); assert(logger_release_checksum(NULL,0U)==UINT32_C(2166136261)); assert(logger_release_checksum(NULL,1U)==0U);",
        "The release computes a deterministic FNV-1a checksum over exactly the serialized record bytes and rejects a missing nonempty input.",
    ),
}
EXERCISES.update(DISTINCT_ALIAS_EXERCISES)


# Final battles combine at least three public operations.  They are small
# release/debugging slices, not ordinary one-function drills with grand names.
FINAL_BATTLE_EXERCISES: dict[str, Exercise] = {
    "gdb-first-steps": exercise(
        "bool sample_sum(const int16_t *samples, size_t count, int32_t *out_sum);\nbool sample_minimum(const int16_t *samples, size_t count, int16_t *out_minimum);\nbool sample_negative_mask(const int16_t *samples, size_t count, uint8_t *out_mask);\nbool sample_window_analyze(const int16_t *samples, size_t count, int32_t *out_sum, int16_t *out_minimum, uint8_t *out_negative_mask);",
        "bool sample_sum(const int16_t *s,size_t n,int32_t *out){if(s==NULL||out==NULL)return false;int32_t total=0;for(size_t i=0U;i<n;++i)total+=s[i];*out=total;return true;}\nbool sample_minimum(const int16_t *s,size_t n,int16_t *out){if(s==NULL||out==NULL||n==0U)return false;int16_t low=s[0];for(size_t i=1U;i<n;++i)if(s[i]<low)low=s[i];*out=low;return true;}\nbool sample_negative_mask(const int16_t *s,size_t n,uint8_t *out){if(s==NULL||out==NULL||n==0U||n>8U)return false;uint8_t mask=0U;for(size_t i=0U;i<n;++i)if(s[i]<0)mask=(uint8_t)(mask|(uint8_t)(UINT8_C(1)<<i));*out=mask;return true;}\nbool sample_window_analyze(const int16_t *s,size_t n,int32_t *sum,int16_t *low,uint8_t *mask){if(s==NULL||n==0U||n>8U||sum==NULL||low==NULL||mask==NULL)return false;int32_t next_sum=0;int16_t next_low=0;uint8_t next_mask=0U;if(!sample_sum(s,n,&next_sum)||!sample_minimum(s,n,&next_low)||!sample_negative_mask(s,n,&next_mask))return false;*sum=next_sum;*low=next_low;*mask=next_mask;return true;}",
        "const int16_t v[]={10,-3,7};int32_t sum=99;int16_t low=99;uint8_t mask=0U;assert(sample_sum(v,3U,&sum)&&sum==14);assert(sample_minimum(v,3U,&low)&&low==-3);assert(sample_negative_mask(v,3U,&mask)&&mask==UINT8_C(0x02));assert(sample_window_analyze(v,3U,&sum,&low,&mask)&&sum==14&&low==-3&&mask==UINT8_C(0x02));assert(!sample_window_analyze(v,0U,&sum,&low,&mask));assert(!sample_window_analyze(v,9U,&sum,&low,&mask));",
        "The debugging release repairs a counted loop, sums and finds the minimum, encodes negative positions in an eight-bit mask, then publishes all results together only after every pointer and extent is valid.",
        starter="#include \"task.h\"\nbool sample_sum(const int16_t *s,size_t n,int32_t *out){if(s==NULL||out==NULL)return false;int32_t total=0;for(size_t i=0U;i<=n;++i)total+=s[i];*out=total;return true;}\n/* Debug the bound, then implement the three missing interfaces. */",
    ),
    "telemetry-cli-release": exercise(
        "bool celsius_in_sensor_range(double celsius);\nbool celsius_to_milli(double celsius, int32_t *out_milli_celsius);\nbool telemetry_prepare(double celsius, bool sensor_fault, int32_t *out_milli_celsius);",
        "bool celsius_in_sensor_range(double c){return c>=-40.0&&c<=125.0;}\nbool celsius_to_milli(double c,int32_t *out){if(out==NULL||!celsius_in_sensor_range(c))return false;const double scaled=c*1000.0;*out=(int32_t)(scaled>=0.0?scaled+0.5:scaled-0.5);return true;}\nbool telemetry_prepare(double c,bool fault,int32_t *out){return !fault&&celsius_to_milli(c,out);}",
        "int32_t v=77;assert(celsius_in_sensor_range(-40.0));assert(!celsius_in_sensor_range(125.1));assert(celsius_to_milli(21.125,&v)&&v==21125);assert(celsius_to_milli(-0.0006,&v)&&v==-1);v=77;assert(telemetry_prepare(3.3,false,&v)&&v==3300);assert(!telemetry_prepare(3.3,true,&v)&&v==3300);",
        "The telemetry release validates the physical range, performs deterministic milli-degree conversion, and refuses to publish a measurement when the sensor reports a fault.",
    ),
    "packet-parser-release": exercise(
        "struct parsed_packet { uint8_t kind; uint16_t value; };\nbool packet_header_valid(const uint8_t *bytes, size_t length);\nbool packet_decode_value(const uint8_t *bytes, size_t length, uint16_t *out_value);\nbool packet_parse(const uint8_t *bytes, size_t length, struct parsed_packet *out_packet);",
        "bool packet_header_valid(const uint8_t *b,size_t n){return b!=NULL&&n==4U&&b[1]==2U&&b[0]<=1U;}\nbool packet_decode_value(const uint8_t *b,size_t n,uint16_t *out){if(!packet_header_valid(b,n)||out==NULL)return false;*out=(uint16_t)((uint16_t)b[2]|((uint16_t)b[3]<<8U));return true;}\nbool packet_parse(const uint8_t *b,size_t n,struct parsed_packet *out){if(out==NULL||!packet_header_valid(b,n))return false;struct parsed_packet parsed={b[0],0U};if(!packet_decode_value(b,n,&parsed.value))return false;*out=parsed;return true;}",
        "const uint8_t good[]={1U,2U,0x34U,0x12U};uint16_t value=0U;struct parsed_packet out={9U,9U};assert(packet_header_valid(good,4U));assert(packet_decode_value(good,4U,&value)&&value==UINT16_C(0x1234));assert(packet_parse(good,4U,&out)&&out.kind==1U&&out.value==UINT16_C(0x1234));const uint8_t bad[]={2U,2U,0U,0U};assert(!packet_header_valid(bad,4U));assert(!packet_parse(good,3U,&out));",
        "The parser release validates the whole frame header, decodes little-endian payload bytes without alignment assumptions, and commits a typed packet only after both stages succeed.",
    ),
    "modular-library-release": exercise(
        "uint8_t crc8_update(uint8_t crc, uint8_t byte);\nuint8_t crc8(const uint8_t *bytes, size_t length);\nbool crc8_verify(const uint8_t *bytes, size_t length, uint8_t expected);",
        "uint8_t crc8_update(uint8_t crc,uint8_t byte){crc^=byte;for(unsigned bit=0U;bit<8U;++bit)crc=(uint8_t)((crc&0x80U)?(uint8_t)(crc<<1U)^0x07U:(uint8_t)(crc<<1U));return crc;}\nuint8_t crc8(const uint8_t *bytes,size_t length){if(bytes==NULL&&length!=0U)return 0U;uint8_t crc=0U;for(size_t i=0U;i<length;++i)crc=crc8_update(crc,bytes[i]);return crc;}\nbool crc8_verify(const uint8_t *bytes,size_t length,uint8_t expected){return(bytes!=NULL||length==0U)&&crc8(bytes,length)==expected;}",
        "const uint8_t data[]={1U,2U,3U};assert(crc8_update(0U,1U)==UINT8_C(0x07));assert(crc8(data,3U)==UINT8_C(0x48));assert(crc8(NULL,0U)==0U);assert(crc8_verify(data,3U,UINT8_C(0x48)));assert(!crc8_verify(data,3U,UINT8_C(0x49)));assert(!crc8_verify(NULL,1U,0U));",
        "The library release exposes a one-byte primitive, a counted-buffer operation, and a verification API through one self-contained header and separately compiled implementation.",
    ),
    "register-driver-release": exercise(
        "bool gpio_pin_valid(unsigned pin);\nbool gpio_mode_set(uint32_t original, unsigned pin, uint32_t mode, uint32_t *out_value);\nbool gpio_mode_matches(uint32_t register_value, unsigned pin, uint32_t expected_mode);",
        "bool gpio_pin_valid(unsigned pin){return pin<16U;}\nbool gpio_mode_set(uint32_t original,unsigned pin,uint32_t mode,uint32_t *out){if(out==NULL||!gpio_pin_valid(pin)||mode>3U)return false;const unsigned shift=pin*2U;const uint32_t mask=UINT32_C(3)<<shift;*out=(original&~mask)|(mode<<shift);return true;}\nbool gpio_mode_matches(uint32_t value,unsigned pin,uint32_t mode){return gpio_pin_valid(pin)&&mode<=3U&&((value>>(pin*2U))&UINT32_C(3))==mode;}",
        "uint32_t out=0U;assert(gpio_pin_valid(15U));assert(!gpio_pin_valid(16U));assert(gpio_mode_set(UINT32_MAX,5U,1U,&out));assert(gpio_mode_matches(out,5U,1U));assert((out&~(UINT32_C(3)<<10U))==(UINT32_MAX&~(UINT32_C(3)<<10U)));assert(!gpio_mode_set(0U,16U,1U,&out));",
        "The register-driver release validates the pin domain, performs a reserved-bit-preserving field update, and reads the configured field back through a separate query.",
    ),
    "peripheral-console-release": exercise(
        "enum console_command { CONSOLE_INVALID, CONSOLE_LED_ON, CONSOLE_LED_OFF, CONSOLE_READ_ADC };\nenum console_command console_parse(const char *line);\nbool console_is_led_command(enum console_command command);\nbool console_led_level(enum console_command command, bool active_low, bool *out_level);",
        "enum console_command console_parse(const char *line){if(line==NULL)return CONSOLE_INVALID;if(strcmp(line,\"LED ON\")==0)return CONSOLE_LED_ON;if(strcmp(line,\"LED OFF\")==0)return CONSOLE_LED_OFF;if(strcmp(line,\"READ ADC\")==0)return CONSOLE_READ_ADC;return CONSOLE_INVALID;}\nbool console_is_led_command(enum console_command command){return command==CONSOLE_LED_ON||command==CONSOLE_LED_OFF;}\nbool console_led_level(enum console_command command,bool active_low,bool *out){if(out==NULL||!console_is_led_command(command))return false;const bool on=command==CONSOLE_LED_ON;*out=active_low?!on:on;return true;}",
        "bool level=false;assert(console_parse(\"LED ON\")==CONSOLE_LED_ON);assert(console_parse(\"READ ADC\")==CONSOLE_READ_ADC);assert(console_is_led_command(CONSOLE_LED_OFF));assert(!console_is_led_command(CONSOLE_READ_ADC));assert(console_led_level(CONSOLE_LED_ON,false,&level)&&level);assert(console_led_level(CONSOLE_LED_ON,true,&level)&&!level);assert(!console_led_level(CONSOLE_READ_ADC,false,&level));assert(console_parse(\"LED\")==CONSOLE_INVALID);",
        "The peripheral-console release parses complete UART text into typed commands, classifies actuator work, and converts a logical LED request to the configured electrical level.",
    ),
    "controller-release": exercise(
        "struct sensor_controller { uint32_t period; uint32_t last_sample; unsigned samples; };\nbool sensor_controller_due(const struct sensor_controller *controller, uint32_t now);\nbool sensor_sample_acceptable(bool sensor_ready, int32_t value, int32_t minimum, int32_t maximum);\nbool sensor_controller_update(struct sensor_controller *controller, uint32_t now, bool sensor_ready);",
        "bool sensor_controller_due(const struct sensor_controller *c,uint32_t now){return c!=NULL&&c->period!=0U&&(uint32_t)(now-c->last_sample)>=c->period;}\nbool sensor_sample_acceptable(bool ready,int32_t value,int32_t minimum,int32_t maximum){return ready&&minimum<=maximum&&value>=minimum&&value<=maximum;}\nbool sensor_controller_update(struct sensor_controller *c,uint32_t now,bool ready){if(!sensor_controller_due(c,now)||!ready)return false;c->last_sample+=c->period;++c->samples;return true;}",
        "struct sensor_controller c={10U,100U,0U};assert(!sensor_controller_due(&c,109U));assert(sensor_controller_due(&c,110U));assert(sensor_sample_acceptable(true,25,-40,125));assert(!sensor_sample_acceptable(false,25,-40,125));assert(!sensor_sample_acceptable(true,126,-40,125));assert(sensor_controller_update(&c,110U,true)&&c.samples==1U&&c.last_sample==110U);assert(!sensor_controller_update(&c,120U,false));",
        "The controller release combines wrap-safe scheduling, bounded sample acceptance, and an explicit state update that counts only ready measurements at a due release.",
    ),
    "incident-response-release": exercise(
        "bool watchdog_elapsed(uint32_t now, uint32_t last_kick, uint32_t timeout);\nbool ring_indices_valid(size_t head, size_t tail, size_t count, size_t capacity);\nbool recovery_required(bool watchdog_expired, bool ring_valid, unsigned consecutive_errors, unsigned error_limit);",
        "bool watchdog_elapsed(uint32_t now,uint32_t last,uint32_t timeout){return timeout!=0U&&(uint32_t)(now-last)>=timeout;}\nbool ring_indices_valid(size_t head,size_t tail,size_t count,size_t capacity){return capacity!=0U&&head<capacity&&tail<capacity&&count<=capacity;}\nbool recovery_required(bool expired,bool ring_valid,unsigned errors,unsigned limit){return expired||!ring_valid||limit==0U||errors>=limit;}",
        "assert(!watchdog_elapsed(109U,100U,10U));assert(watchdog_elapsed(110U,100U,10U));assert(watchdog_elapsed(3U,UINT32_MAX-5U,8U));assert(ring_indices_valid(3U,1U,2U,4U));assert(!ring_indices_valid(4U,0U,0U,4U));assert(!recovery_required(false,true,2U,3U));assert(recovery_required(true,true,0U,3U));assert(recovery_required(false,false,0U,3U));assert(recovery_required(false,true,3U,3U));",
        "The incident-response release reproduces wraparound timeout behavior, checks a persisted ring invariant, and makes one explicit recovery decision from independent fault evidence.",
    ),
    "rtos-concepts": exercise(
        "bool startup_services_ready(bool memory_ready, bool drivers_ready, bool scheduler_ready);\nbool queue_absorbs_burst(size_t producer_burst, size_t consumer_progress, size_t queue_capacity);\nbool periodic_load_fits(uint32_t execution_us, uint32_t blocking_us, uint32_t period_us);\nbool rtos_partition_justified(unsigned independent_jobs, bool shared_blocking_io, bool cooperative_deadlines_met);",
        "bool startup_services_ready(bool memory,bool drivers,bool scheduler){return memory&&drivers&&scheduler;}\nbool queue_absorbs_burst(size_t produced,size_t consumed,size_t capacity){return produced<=consumed||produced-consumed<=capacity;}\nbool periodic_load_fits(uint32_t execution,uint32_t blocking,uint32_t period){return execution<=period&&blocking<=period-execution;}\nbool rtos_partition_justified(unsigned jobs,bool blocking_io,bool cooperative_ok){return jobs>=2U&&(blocking_io||!cooperative_ok);}",
        "assert(startup_services_ready(true,true,true));assert(!startup_services_ready(true,false,true));assert(queue_absorbs_burst(8U,3U,5U));assert(!queue_absorbs_burst(9U,3U,5U));assert(periodic_load_fits(200U,100U,1000U));assert(!periodic_load_fits(900U,200U,1000U));assert(rtos_partition_justified(3U,true,true));assert(rtos_partition_justified(2U,false,false));assert(!rtos_partition_justified(1U,true,false));assert(!rtos_partition_justified(3U,false,true));",
        "The architecture battle gates scheduler startup on ready memory and drivers, checks queue burst capacity and execution-plus-blocking deadlines, then decides whether separate RTOS tasks justify their complexity.",
    ),
    "data-logger-release": exercise(
        "bool logger_record_shape_valid(const uint8_t *bytes, size_t length);\nuint32_t logger_release_checksum(const uint8_t *bytes, size_t length);\nbool logger_release_validate(const uint8_t *bytes, size_t length, uint32_t expected_checksum);",
        "bool logger_record_shape_valid(const uint8_t *bytes,size_t length){return bytes!=NULL&&length>=3U&&bytes[0]==1U&&bytes[1]==(uint8_t)(length-2U);}\nuint32_t logger_release_checksum(const uint8_t *bytes,size_t length){uint32_t hash=UINT32_C(2166136261);if(bytes==NULL&&length!=0U)return 0U;for(size_t i=0U;i<length;++i){hash^=bytes[i];hash*=UINT32_C(16777619);}return hash;}\nbool logger_release_validate(const uint8_t *bytes,size_t length,uint32_t expected){return logger_record_shape_valid(bytes,length)&&logger_release_checksum(bytes,length)==expected;}",
        "const uint8_t record[]={1U,1U,42U};assert(logger_record_shape_valid(record,3U));assert(!logger_record_shape_valid(record,2U));assert(logger_release_checksum(record,3U)==UINT32_C(399283687));assert(logger_release_validate(record,3U,UINT32_C(399283687)));assert(!logger_release_validate(record,3U,0U));const uint8_t wrong[]={2U,1U,42U};assert(!logger_record_shape_valid(wrong,3U));assert(logger_release_checksum(NULL,0U)==UINT32_C(2166136261));",
        "The capstone release validates a versioned record shape, hashes exactly the serialized bytes, and accepts a record only when structure and integrity evidence both pass.",
    ),
}
EXERCISES.update(FINAL_BATTLE_EXERCISES)


HARNESS_SUPPORT: dict[str, str] = {
    "callbacks": "static bool capture_status(void *context,uint8_t value){*(unsigned *)context += value;return true;}",
    "function-pointers": "static bool capture_handler(void *context,uint8_t value){*(unsigned *)context += value;return true;}",
    "hal-design": "struct fake_hal{int32_t value;bool alarm;bool read_ok;}; static bool fake_read(void *c,int32_t *out){struct fake_hal *f=c;if(!f->read_ok)return false;*out=f->value;return true;} static void fake_alarm(void *c,bool on){((struct fake_hal *)c)->alarm=on;}",
    "integration-testing": "struct fake_logger{bool read_ok,store_ok;int32_t value,stored;unsigned reads,writes;}; static bool fake_logger_read(void *c,int32_t *out){struct fake_logger *f=c;++f->reads;if(!f->read_ok)return false;*out=f->value;return true;} static bool fake_logger_store(void *c,int32_t v){struct fake_logger *f=c;++f->writes;if(!f->store_ok)return false;f->stored=v;return true;}",
    "sensor-interface": "struct fake_sensor{enum sensor_status status;int32_t value;}; static enum sensor_status fake_sensor_read(void *c,int32_t *out){struct fake_sensor *f=c;if(f->status==SENSOR_OK)*out=f->value;return f->status;}",
    "timestamp-injection": "static uint32_t fake_clock(void *context){return *(uint32_t *)context;}",
    "storage-interface": "struct fake_storage{uint8_t bytes[16];size_t length,chunk;bool fail;}; static size_t fake_storage_write(void *c,const uint8_t *b,size_t n){struct fake_storage *s=c;if(s->fail)return 0U;size_t take=n<s->chunk?n:s->chunk;memcpy(s->bytes+s->length,b,take);s->length+=take;return take;}",
    "transport-retry": "struct fake_transport{unsigned temporary_left,calls;enum transport_status final;}; static enum transport_status fake_transport_send(void *c){struct fake_transport *t=c;++t->calls;if(t->temporary_left!=0U){--t->temporary_left;return TRANSPORT_TEMPORARY;}return t->final;}",
    "data-logger-integration": "struct integration_fake{int32_t value;uint32_t tick;enum logger_io read_result,store_result,send_results[4];size_t send_count,send_index;unsigned store_calls,send_calls;}; static enum logger_io integration_read(void *c,int32_t *out){struct integration_fake *f=c;if(f->read_result==LOGGER_IO_OK)*out=f->value;return f->read_result;} static uint32_t integration_now(void *c){return ((struct integration_fake *)c)->tick;} static enum logger_io integration_store(void *c,const uint8_t *b,size_t n){struct integration_fake *f=c;(void)b;(void)n;++f->store_calls;return f->store_result;} static enum logger_io integration_send(void *c,const uint8_t *b,size_t n){struct integration_fake *f=c;(void)b;(void)n;++f->send_calls;if(f->send_index<f->send_count)return f->send_results[f->send_index++];return LOGGER_IO_OK;}",
}

SIM_SUPPORT: dict[str, tuple[tuple[str, ...], tuple[str, ...], str, str]] = {
    "memory-mapped-io": (("platforms/host/src/sim_mmio.c",), ("sim_mmio.h",), "", "sim_mmio_reset(); assert(sim_mmio_write(4U,UINT32_C(0xf0))==SIM_MMIO_OK); uint32_t mmio=0U; assert(sim_mmio_read(4U,&mmio)==SIM_MMIO_OK); volatile uint32_t work=mmio; assert(register_update(&work,UINT32_C(0x30),UINT32_C(0x05))); assert(sim_mmio_write(4U,work)==SIM_MMIO_OK); assert(sim_mmio_read(4U,&mmio)==SIM_MMIO_OK&&mmio==UINT32_C(0xc5));"),
    "register-driver-release": (("platforms/host/src/sim_mmio.c",), ("sim_mmio.h",), "", "sim_mmio_reset(); assert(sim_mmio_write(1U,UINT32_MAX)==SIM_MMIO_OK); uint32_t current=0U,configured=0U; assert(sim_mmio_read(1U,&current)==SIM_MMIO_OK); assert(gpio_mode_set(current,5U,1U,&configured)); assert(sim_mmio_write(1U,configured)==SIM_MMIO_OK); assert(sim_mmio_read(1U,&current)==SIM_MMIO_OK&&((current>>10U)&3U)==1U);"),
    "gpio": (("platforms/host/src/sim_gpio.c",), ("sim_gpio.h",), "", "sim_gpio_reset(); assert(sim_gpio_configure(5U,SIM_GPIO_OUTPUT)==SIM_GPIO_OK); assert(sim_gpio_write(5U,gpio_output_level(true,true)?SIM_GPIO_HIGH:SIM_GPIO_LOW)==SIM_GPIO_OK); enum sim_gpio_level observed=SIM_GPIO_HIGH; assert(sim_gpio_read(5U,&observed)==SIM_GPIO_OK&&observed==SIM_GPIO_LOW); assert(sim_gpio_write(SIM_GPIO_PIN_COUNT,SIM_GPIO_HIGH)==SIM_GPIO_RANGE);"),
    "interrupts": (("platforms/host/src/sim_interrupt.c",), ("sim_interrupt.h",), "static void dispatch_to_mailbox(void *context,uint32_t event){interrupt_capture(context,event);}", "struct interrupt_mailbox simulated={0U,false}; uint32_t captured=0U; sim_interrupt_reset(); assert(sim_interrupt_register(1U,dispatch_to_mailbox,&simulated)==SIM_INTERRUPT_OK); assert(sim_interrupt_trigger(1U,23U)==SIM_INTERRUPT_DISABLED); assert(sim_interrupt_enable(1U,true)==SIM_INTERRUPT_OK); assert(sim_interrupt_trigger(1U,23U)==SIM_INTERRUPT_OK); assert(interrupt_take(&simulated,&captured)&&captured==23U);"),
    "timers": (("platforms/host/src/sim_timer.c",), ("sim_timer.h",), "", "sim_timer_reset(UINT32_MAX-2U); sim_timer_advance(5U); assert(deadline_reached(sim_timer_now(),UINT32_MAX-2U)); assert(sim_timer_elapsed(UINT32_MAX-2U)==5U);"),
    "nonblocking-time": (("platforms/host/src/sim_timer.c",), ("sim_timer.h",), "", "struct blinker timed={UINT32_MAX-2U,5U,false}; sim_timer_reset(UINT32_MAX-2U); sim_timer_advance(5U); assert(blinker_update(&timed,sim_timer_now())&&timed.level);"),
    "uart": (("platforms/host/src/sim_uart.c",), ("sim_uart.h",), "", "const uint8_t received[]={'O','K','\\n'}; struct uart_line simulated={{0},0U}; uint8_t incoming=0U; sim_uart_reset(); assert(sim_uart_inject_rx(received,sizeof received)==SIM_UART_OK); while(sim_uart_read(&incoming)==SIM_UART_OK)(void)uart_line_feed(&simulated,(char)incoming); assert(strcmp(simulated.bytes,\"OK\")==0); assert(sim_uart_write((const uint8_t *)simulated.bytes,simulated.length)==SIM_UART_OK&&sim_uart_tx_pending()==2U);"),
    "adc": (("platforms/host/src/sim_adc.c",), ("sim_adc.h",), "", "uint16_t raw=0U,scaled=0U; sim_adc_reset(); assert(sim_adc_set(2U,2048U)==SIM_ADC_OK); assert(sim_adc_read(2U,&raw)==SIM_ADC_OK); assert(adc_code_to_mv(raw,12U,3300U,&scaled)&&scaled==1650U); assert(sim_adc_set(2U,4096U)==SIM_ADC_RANGE);"),
    "pwm": (("platforms/host/src/sim_pwm.c",), ("sim_pwm.h",), "", "uint32_t calculated=0U,period=0U,observed=0U; sim_pwm_reset(); assert(pwm_compare(1000U,25U,&calculated)); assert(sim_pwm_configure(0U,1000U,calculated)==SIM_PWM_OK); assert(sim_pwm_observe(0U,&period,&observed)==SIM_PWM_OK&&period==1000U&&observed==250U); assert(sim_pwm_configure(0U,10U,11U)==SIM_PWM_ARGUMENT);"),
    "spi": (("platforms/host/src/sim_spi.c",), ("sim_spi.h",), "", "uint8_t built[2]={0U},rx_bytes[2]={0U}; size_t built_count=0U; const uint8_t reply[]={0U,UINT8_C(0x5a)}; sim_spi_reset(); assert(spi_build_read(UINT8_C(0x12),built,sizeof built,&built_count)); assert(sim_spi_set_response(reply,sizeof reply)==SIM_SPI_OK); assert(sim_spi_transfer(built,rx_bytes,built_count)==SIM_SPI_NOT_SELECTED); sim_spi_select(true); assert(sim_spi_transfer(built,rx_bytes,built_count)==SIM_SPI_OK&&rx_bytes[1]==UINT8_C(0x5a));"),
    "i2c": (("platforms/host/src/sim_i2c.c",), ("sim_i2c.h",), "", "const uint8_t device_regs[]={UINT8_C(0x10),UINT8_C(0x42)}; uint8_t address_byte=0U,sample=0U; sim_i2c_reset(); assert(i2c_address_byte(UINT8_C(0x48),true,&address_byte)&&address_byte==UINT8_C(0x91)); assert(sim_i2c_attach(UINT8_C(0x48),device_regs,sizeof device_regs)==SIM_I2C_OK); assert(sim_i2c_read_register((uint8_t)(address_byte>>1U),1U,&sample)==SIM_I2C_OK&&sample==UINT8_C(0x42)); sim_i2c_fail_next(SIM_I2C_TIMEOUT); assert(sim_i2c_read_register(UINT8_C(0x48),1U,&sample)==SIM_I2C_TIMEOUT);"),
    "peripheral-console-release": (("platforms/host/src/sim_uart.c", "platforms/host/src/sim_gpio.c"), ("sim_uart.h", "sim_gpio.h"), "", "const uint8_t command[]={'L','E','D',' ','O','N'}; uint8_t line[7]={0U}; sim_uart_reset(); sim_gpio_reset(); assert(sim_uart_inject_rx(command,sizeof command)==SIM_UART_OK); for(size_t index=0U;index<sizeof command;++index)assert(sim_uart_read(&line[index])==SIM_UART_OK); assert(console_parse((const char *)line)==CONSOLE_LED_ON); assert(sim_gpio_configure(5U,SIM_GPIO_OUTPUT)==SIM_GPIO_OK); assert(sim_gpio_write(5U,SIM_GPIO_HIGH)==SIM_GPIO_OK); enum sim_gpio_level led=SIM_GPIO_LOW; assert(sim_gpio_read(5U,&led)==SIM_GPIO_OK&&led==SIM_GPIO_HIGH);"),
}


CASE_FACTS = {
    "workstation-orientation": "A boot coordinator calls `firmware_status` before enabling later modules. A count of zero must report not-ready, while one or any larger unsigned count reports success; the trusted driver owns `main`, so this source file contributes only the promised definition.",
    "source-to-program": "A missing declaration is diagnosed while compiling its consumer, a missing definition appears while linking, and preprocessing output contains expanded headers but no linked addresses.",
    "binary-and-hex": "For the worked value 0xA5, bits 7, 5, 2, and 0 are set, so the decimal sum is 128 + 32 + 4 + 1 = 165; grouping into nibbles makes the binary form 1010 0101.",
    "integer-types": "A signed temperature spanning -40000 to 125000 milli-degrees needs `int32_t`; a 12-bit ADC code fits `uint16_t`; a byte count used with arrays should be `size_t`; protocol fields use exact widths.",
    "floating-point-tradeoffs": "Representing Celsius as signed milli-degrees makes 21.375 C exactly 21375, provides deterministic comparison and serialization, and requires widened intermediates when scaling raw ADC values.",
    "scope-and-storage": "A loop index remains block-local, a module calibration table can have internal linkage with file-scope `static`, and mutable state should not be static inside a reusable function when callers need independent instances.",
    "decomposition": "The telemetry ticket separates parse, validate, convert, format, and transport operations; each returns an explicit status so invalid text cannot be confused with a valid zero measurement.",
    "memory-lifetime": "Returning the address of an automatic local object is invalid after return; caller-owned output, immutable static data, or caller-supplied storage each make a different valid lifetime contract.",
    "alignment-endianness": "Bytes 78 56 34 12 decode to 0x12345678 in the stated little-endian protocol; shifting `uint8_t` values into `uint32_t` avoids unaligned access, padding, aliasing, and host-order assumptions.",
    "pointer-parameters": "A two-byte sensor payload arrives as the octets 0x34 and 0x12. The decoder first proves that the readable span contains both octets, combines them in little-endian order, and writes 0x1234 through `out_value`; a short span or absent address leaves the caller's destination untouched.",
    "dynamic-memory-policy": "The selected policy uses a fixed pool initialized at boot, rejects exhaustion explicitly, keeps allocation out of interrupt context, and assigns each block a single owner until an explicit release.",
    "preprocessor-discipline": "The macro `SQUARE(x)` can evaluate `x` twice and needs parentheses; an inline function gives one evaluation and type checking, while include guards prevent duplicate declarations rather than duplicate external definitions.",
    "cpu-memory-model": "A load-modify-store sequence copies a memory-mapped register value into a CPU register, changes the local value, then performs an observable store; CPU registers and peripheral registers are different objects.",
    "const-and-volatile": "`const uint8_t *` protects bytes through that view, `volatile uint32_t *` preserves observable register accesses, and neither qualifier supplies atomicity or interrupt synchronization.",
    "electronics-basics": "The LED output needs a current-limiting path and a known active level; a button input needs a pull resistor; an I2C line uses open-drain output with a pull-up rather than push-pull high drive.",
    "datasheet-reading": "The extraction table records register offset, reset value, access mode, field mask and shift, reserved-bit policy, and the required enable/configure/clear sequence before code is written.",
    "interrupts": "The ISR captures one event into bounded shared state and returns; formatting, parsing, and transport move to foreground work, with ownership or a critical section defined for every shared update.",
    "stm32-toolchain-checkpoint": "The read-only doctor distinguishes the ARM compiler, debugger, OpenOCD or CubeProgrammer, and ordinary host tools; missing tools are setup facts and do not trigger a flash attempt.",
    "stm32-board-checkpoint": "The NUCLEO-C031C6 checkpoint uses the documented PA5 user LED and USART2 PA2/PA3 virtual COM path; flashing remains an explicit confirmed action and observations are recorded separately from host tests.",
    "callbacks": "The callback signature carries a `void *context`, the owner guarantees that context outlives registration, null callbacks are rejected, and interrupt-context restrictions are part of the contract.",
    "configuration": "Buffer capacity and compiled feature presence are compile-time constraints; sample period and thresholds are runtime configuration validated once before the controller starts.",
    "resource-constraints": "The budget lists static RAM, worst-case stack, queue storage, flash, and worst-case handler time; queue depth and stack depth are dominant assumptions and receive explicit margins.",
    "static-analysis": "An unchecked null dereference is repaired, a signed/unsigned comparison is normalized to one validated representation, and a suppression is accepted only with tool rule, local rationale, and an executable invariant.",
    "concurrency": "A single producer ISR and single consumer foreground loop can exchange indices only under a documented atomic-width assumption; multi-field records need commit ownership, not merely `volatile`.",
    "secure-c": "The decoder validates the received buffer length before trusting an internal length field, checks integer conversions before allocation or indexing, decodes into temporary state, and commits only after the whole frame passes.",
    "portability": "A four-octet wire field must decode identically on x86 and Cortex-M0+: 78 56 34 12 becomes 0x12345678. Explicit byte loads and shifts avoid a casted `uint32_t` access, so the result does not depend on native byte order, address alignment, structure padding, or effective-type aliasing rules.",
    "api-design": "The public queue API exposes status-returning init, push, pop, capacity, and count operations while representation, indices, and invariant repair remain private implementation details.",
    "semantic-versioning": "Fixing an internal wrap bug without contract change is a patch; adding a backward-compatible query is minor; changing queue-full behavior or a public signature is major and requires migration notes.",
    "library-configuration": "A validated initialization structure chooses caller-provided capacity and policy, defaults are explicit, invalid combinations fail at initialization, and feature macros alter platform integration rather than core semantics.",
    "library-documentation": "Each public call documents nullability, ownership, lifetime, interrupt/thread context, mutation, full/empty behavior, return status, and one minimal consumer sequence from storage allocation through pop.",
    "library-testing": "The matrix covers empty, one item, full, wraparound, invalid pointers, smallest and largest configurations, repeated initialization, separate compilation, and a consumer that sees only installed public headers.",
    "packaging": "The concrete `library/record_queue` project installs public headers under `include`, the archive under `lib`, exports CMake metadata, and proves relocation by building `examples/library-consumer` against a temporary prefix with no source-tree include path.",
    "consumer-integration-release": "Release evidence for `library/record_queue` combines strict unit tests, Make and CMake consumers, temporary-prefix installation, public-header self-containment, version reporting, API documentation, and a clean rebuild.",
    "startup-code": "Reset selects the vector entry, establishes stack state, copies initialized data from flash to RAM, zeros BSS, performs system setup, and only then calls `main`; constructors are toolchain policy, not peripheral initialization.",
    "linker-scripts": "FLASH origin and length bound text/rodata plus initial data images; RAM bounds data, BSS, heap if used, and stack; linker symbols expose copy and zero ranges to startup code.",
    "memory-sections": "Executable code belongs in text, immutable tables in rodata, initialized mutable state in data, zero-initialized state in BSS, and retained crash information in a deliberately initialized noinit region.",
    "boot-flow": "Outputs first enter a hardware-safe state, reset cause and retained diagnostics are captured, clocks and memory are established, configuration is validated, drivers start in dependency order, and only then are actuators enabled.",
    "real-time-analysis": "Worst-case execution times are compared with periods and blocking; utilization alone does not prove deadlines when a long non-preemptive handler delays a short-period task.",
    "rtos-concepts": "The RTOS alternative gives acquisition, storage, and transport separate tasks joined by bounded queues; shared device access needs ownership, but a small cooperative loop remains preferable when bounded handlers already meet deadlines.",
    "capstone-requirements": "Requirements specify sample period and jitter, accepted ranges, reject-new buffer behavior, versioned byte order, storage and retry failures, RAM budget, no dynamic allocation after startup, and host-verifiable acceptance tests.",
    "capstone-architecture": "Acquisition, validation, timestamping, buffering, serialization, storage, and transport communicate through typed interfaces; only board adapters know STM32 HAL types or registers.",
    "data-logger-integration": "The integration plan runs nominal capture/export, invalid sample rejection, full queue, wraparound, partial storage, temporary transport retry, permanent failure, and deterministic time scenarios before the board adapter is attached.",
    "data-logger-release": "The concrete `capstone/reference` release packages public headers and portable sources, documents ownership and wire compatibility, publishes strict host tests and a demo, and leaves clock, sensor, storage, transport, and STM32 choices behind adapters.",
}


def _mission_directory(mission_id: str) -> Path:
    curriculum_root = Path(
        os.environ.get("LEARN_C_CURRICULUM_ROOT", str(curriculum_source.CURRICULUM))
    ).resolve()
    matches = [
        manifest.parent
        for manifest in curriculum_root.rglob("level.toml")
        if manifest.parent.name.split("-", 1)[-1] == mission_id
    ]
    if len(matches) != 1:
        raise RuntimeError(f"expected one package for {mission_id}, found {len(matches)}")
    return matches[0]


def _header(mission: MissionDef, declarations: str) -> str:
    guard = f"LEARN_{mission.id.upper().replace('-', '_')}_TASK_H"
    return f"""#ifndef {guard}
#define {guard}

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

{declarations}

#endif
"""


def _source(implementation: str) -> str:
    return f"""#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

{implementation}
"""


def _harness(mission_id: str, tests: str) -> str:
    support = HARNESS_SUPPORT.get(mission_id, "")
    sim_headers = ""
    sim_support = ""
    sim_tests = ""
    if mission_id in SIM_SUPPORT:
        _, headers, sim_support, sim_tests = SIM_SUPPORT[mission_id]
        sim_headers = "\n".join(f'#include "{header}"' for header in headers)
    return f"""#include "task.h"
{sim_headers}

#include <assert.h>
#include <limits.h>
#include <string.h>

{support}
{sim_support}

int main(void) {{
    {tests}
    {sim_tests}
    return 0;
}}
"""


def _visible_function_wrappers(declarations: str, tests: str) -> str:
    """Instrument direct public calls while preserving each function's return type."""
    signatures = re.findall(
        r"(?:^|\n)\s*([^\n;{}()]+?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^;{}]*)\)\s*;",
        declarations,
    )
    wrappers: list[str] = []
    for return_type, name, _ in signatures:
        return_type = return_type.strip()
        if not re.search(rf"\b{re.escape(name)}\s*\(", tests):
            continue
        call_text = f'"{name}(" #__VA_ARGS__ ")"'
        if return_type == "void":
            wrappers.append(
                f'#define {name}(...) (printf("Call and inputs: %s\\n  Actual return: void\\n", {call_text}), ({name})(__VA_ARGS__))'
            )
            continue
        helper = f"visible_return_{name}"
        if return_type == "bool":
            body = (
                'printf("Call and inputs: %s\\n  Actual return: %s\\n", '
                'call, value ? "true" : "false");'
            )
        elif return_type.startswith("uint") or return_type in {"size_t", "unsigned"}:
            body = (
                'printf("Call and inputs: %s\\n  Actual return: %llu\\n", '
                'call, (unsigned long long)value);'
            )
        else:
            body = (
                'printf("Call and inputs: %s\\n  Actual return: %lld\\n", '
                'call, (long long)value);'
            )
        wrappers.append(
            f"static {return_type} {helper}(const char *call, {return_type} value) {{ {body} return value; }}\n"
            f"#define {name}(...) {helper}({call_text}, ({name})(__VA_ARGS__))"
        )
    return "\n".join(wrappers)


def _visible_harness(mission_id: str, declarations: str, tests: str) -> str:
    support = HARNESS_SUPPORT.get(mission_id, "")
    sim_headers = ""
    sim_support = ""
    sim_tests = ""
    if mission_id in SIM_SUPPORT:
        _, headers, sim_support, sim_tests = SIM_SUPPORT[mission_id]
        sim_headers = "\n".join(f'#include "{header}"' for header in headers)
    all_tests = tests + "\n" + sim_tests
    wrappers = _visible_function_wrappers(declarations, all_tests)
    case_count = all_tests.count("assert(")
    if case_count < 1:
        raise RuntimeError(f"visible harness for {mission_id} has no cases")
    return f"""#include "task.h"
{sim_headers}

#include <limits.h>
#include <stdio.h>
#include <string.h>

{support}
{sim_support}
{wrappers}

#define VISIBLE_CASE_COUNT {case_count}

static unsigned visible_case_number;
static unsigned visible_failures;

static void visible_check(int passed, const char *expression) {{
    printf("Case %u\\n  Expected condition: %s\\n  Observed condition: %s\\n  Result: %s\\n",
           visible_case_number, expression, passed ? "true" : "false",
           passed ? "PASS" : "FAIL");
    if (!passed) ++visible_failures;
}}

#define assert(expression) do {{ \
    ++visible_case_number; \
    visible_check(!!(expression), #expression); \
}} while (0)

int main(void) {{
    {tests}
    {sim_tests}
    printf("Visible run: %u cases checked; %u failed.\\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}}
"""


def _analysis_answer(mission: MissionDef) -> str:
    concepts = ", ".join(mission.concepts)
    fact = CASE_FACTS.get(mission.id, mission.assignment)
    return f"""# {mission.title} — Model Engineering Analysis

## Prediction

The proposed work must satisfy this ticket: {mission.assignment} I predict the design will remain dependable only when {concepts} are represented as explicit contracts rather than comments added after implementation. A normal example should demonstrate the intended outcome, while one deliberately failing example should show the exact boundary and status visible to the caller. Any hardware observation is evidence about an adapter, not proof that portable policy is correct.

## Evidence

{fact} The evidence package should preserve inputs, expected outputs or states, the command or trace that produced the observation, and the first relevant diagnostic when something fails. For each of {concepts}, I would identify which object owns the state and how its valid range or lifetime is established. This makes the argument reviewable instead of depending on a successful-looking printout.

## Decision

I would accept the work only with a narrow interface, named failure behavior, and repeatable evidence that directly exercises the assignment. The implementation or design should keep portable decisions separate from terminal, operating-system, or STM32 effects. Every mutable object has one owner at a time; conversions occur only after range checks; and an unavailable dependency returns a typed failure rather than a plausible data value. These choices make later refactoring and library reuse possible.

## Boundary Cases

The review must cover empty or zero work, the smallest valid case, a typical case, the largest representable or configured case, and the first invalid case. It must also consider null or absent dependencies, partial progress, repeated calls, counter wrap where time is involved, and recovery after a reported failure. For hardware work, disconnected tools and a reset during the operation are recorded separately. A boundary that cannot occur should be justified by an enforced upstream invariant, not omitted silently.
"""


def _starter_analysis(mission: MissionDef) -> str:
    questions = "\n".join(f"- What exact claim about **{concept}** will your evidence support?" for concept in mission.concepts)
    return f"""# {mission.title} — Engineering Analysis

Use the lesson and case file to answer the ticket. Replace every prompt with your own reasoning; a heading by itself is not enough.

## Prediction

State the result you expect before inspecting or changing the system.

## Evidence

{questions}

Record concrete values, traces, commands, calculations, or cited board facts here.

## Decision

Choose an implementation or policy and connect it to the evidence.

## Boundary Cases

Cover normal, limiting, invalid, unavailable, and recovery behavior that applies to this ticket.
"""


def _concept_groups(mission: MissionDef) -> list[list[str]]:
    groups: list[list[str]] = []
    for concept in mission.concepts[:3]:
        alternatives = [concept]
        first = concept.replace("/", " ").split()[0]
        if first.casefold() != concept.casefold():
            alternatives.append(first)
        groups.append(alternatives)
    return groups


def _reasoning_check(mission: MissionDef, path: str, check_id: str = "engineering-reasoning") -> str:
    groups = json.dumps(_concept_groups(mission))
    return f"""[[checks]]
id = {json.dumps(check_id)}
name = "Mission-specific evidence and boundary reasoning"
type = "markdown_response"
path = {json.dumps(path)}
headings = ["Prediction", "Evidence", "Decision", "Boundary Cases"]
minimum_words = 180
minimum_section_words = 35
minimum_unique_words = 70
maximum_word_fraction = 0.08
required_concept_groups = {groups}
required = true"""


def _write_reasoning_files(directory: Path, mission: MissionDef, path: str) -> str:
    answer = _analysis_answer(mission)
    (directory / "starter" / path).write_text(_starter_analysis(mission), encoding="utf-8")
    (directory / "reference" / path).write_text(answer, encoding="utf-8")
    return answer


def _project_makefile() -> str:
    return """CC ?= cc
AR ?= ar
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -O2
PREFIX ?= /usr/local
.PHONY: all clean install
all: librq.a
rq.o: rq.c rq.h
\t$(CC) $(CFLAGS) -c rq.c -o rq.o
librq.a: rq.o
\t$(AR) rcs $@ $^
install: librq.a rq.h
\tmkdir -p $(PREFIX)/include $(PREFIX)/lib
\tcp rq.h $(PREFIX)/include/rq.h
\tcp librq.a $(PREFIX)/lib/librq.a
clean:
\trm -f rq.o librq.a
"""


def _project_cmake() -> str:
    return """cmake_minimum_required(VERSION 3.16)
project(rq VERSION 1.0.0 LANGUAGES C)
add_library(rq STATIC rq.c)
target_include_directories(rq PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}> $<INSTALL_INTERFACE:include>)
target_compile_features(rq PUBLIC c_std_11)
if(CMAKE_C_COMPILER_ID MATCHES \"GNU|Clang\")
  target_compile_options(rq PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()
install(TARGETS rq ARCHIVE DESTINATION lib)
install(FILES rq.h DESTINATION include)
"""


def _project_harness_source() -> str:
    return """from pathlib import Path
import subprocess
import sys

learner = Path(sys.argv[1])
build = Path(sys.argv[2])

def run(argv):
    completed = subprocess.run(argv, text=True, capture_output=True, check=False)
    if completed.returncode:
        print(completed.stdout, end='')
        print(completed.stderr, end='', file=sys.stderr)
        raise SystemExit(completed.returncode)

make_prefix = build / 'make-prefix'
run(['make', '-C', str(learner), 'clean', 'all', 'install', f'PREFIX={make_prefix}'])
cmake_build = build / 'cmake-build'
cmake_prefix = build / 'cmake-prefix'
run(['cmake', '-S', str(learner), '-B', str(cmake_build), f'-DCMAKE_INSTALL_PREFIX={cmake_prefix}'])
run(['cmake', '--build', str(cmake_build)])
run(['cmake', '--install', str(cmake_build)])
consumer = build / 'consumer.c'
consumer.write_text('#include <rq.h>\\n#include <string.h>\\nint main(void){return strcmp(rq_version(),\"1.0.0\");}\\n')
exe = build / 'consumer'
run(['cc', '-std=c11', '-Wall', '-Wextra', '-Wpedantic', '-Werror', f'-I{cmake_prefix / "include"}', str(consumer), str(cmake_prefix / 'lib' / 'librq.a'), '-o', str(exe)])
run([str(exe)])
print('Make build/install and CMake relocated consumer passed')
"""


def _write_packaging_project(directory: Path, mission: MissionDef) -> tuple[str, str]:
    (directory / "checks").mkdir(parents=True, exist_ok=True)
    header = '#ifndef RQ_H\n#define RQ_H\nconst char *rq_version(void);\n#endif\n'
    starter_source = '#include "rq.h"\nconst char *rq_version(void) { return "0.0.0"; }\n'
    reference_source = '#include "rq.h"\nconst char *rq_version(void) { return "1.0.0"; }\n'
    for area, source in (("starter", starter_source), ("reference", reference_source)):
        root = directory / area
        (root / "rq.h").write_text(header, encoding="utf-8")
        (root / "rq.c").write_text(source, encoding="utf-8")
        (root / "Makefile").write_text(_project_makefile(), encoding="utf-8")
        (root / "CMakeLists.txt").write_text(_project_cmake(), encoding="utf-8")
    (directory / "checks" / "verify_project.py").write_text(_project_harness_source(), encoding="utf-8")
    checks = """[[checks]]
id = "package-build-install-consume"
name = "Make and CMake package plus relocated consumer"
type = "project_harness"
harness = "checks/verify_project.py"
timeout = 60
required = true"""
    return checks, f"```c\n{reference_source}```"


def _consumer_harness_source() -> str:
    return """from pathlib import Path
import subprocess
import sys

learner = Path(sys.argv[1])
build = Path(sys.argv[2])
prefix = build / 'installed'
(prefix / 'include').mkdir(parents=True)
(prefix / 'lib').mkdir(parents=True)
(prefix / 'include' / 'rq.h').write_text(
    '#ifndef RQ_H\\n#define RQ_H\\nconst char *rq_version(void);\\nint rq_add(int left,int right);\\n#endif\\n'
)
implementation = build / 'rq.c'
implementation.write_text(
    '#include "rq.h"\\nconst char *rq_version(void){return "1.0.0";}\\nint rq_add(int left,int right){return left+right;}\\n'
)
obj = build / 'rq.o'
archive = prefix / 'lib' / 'librq.a'

def run(argv):
    completed = subprocess.run(argv, text=True, capture_output=True, check=False)
    if completed.returncode:
        print(completed.stdout, end='')
        print(completed.stderr, end='', file=sys.stderr)
        raise SystemExit(completed.returncode)

flags = ['-std=c11', '-Wall', '-Wextra', '-Wpedantic', '-Werror']
run(['cc', *flags, '-I', str(prefix / 'include'), '-c', str(implementation), '-o', str(obj)])
run(['ar', 'rcs', str(archive), str(obj)])
executable = build / 'consumer'
run(['cc', *flags, '-I', str(prefix / 'include'), str(learner / 'consumer.c'), str(archive), '-o', str(executable)])
run([str(executable)])
print('Relocated consumer compiled, linked, and ran against installed-only paths')
"""


def _write_consumer_project(directory: Path, mission: MissionDef) -> tuple[str, str]:
    (directory / "checks").mkdir(parents=True, exist_ok=True)
    starter = """#include <rq.h>

int main(void) {
    /* TODO: verify the installed API and return zero only when it is correct. */
    return 1;
}
"""
    reference = """#include <rq.h>
#include <string.h>

int main(void) {
    if (strcmp(rq_version(), "1.0.0") != 0) return 1;
    if (rq_add(19, 23) != 42) return 2;
    return 0;
}
"""
    (directory / "starter" / "consumer.c").write_text(starter, encoding="utf-8")
    (directory / "reference" / "consumer.c").write_text(reference, encoding="utf-8")
    (directory / "checks" / "verify_consumer.py").write_text(
        _consumer_harness_source(), encoding="utf-8"
    )
    checks = """[[checks]]
id = "installed-consumer"
name = "Strict relocated consumer against installed header and archive"
type = "project_harness"
harness = "checks/verify_consumer.py"
timeout = 30
required = true"""
    return checks, f"```c\n{reference}```"


def _write_first_program(directory: Path, mission: MissionDef) -> tuple[str, str]:
    starter = '#include <stdio.h>\nint main(void) { puts("firmware pending"); return 1; }\n'
    reference = '#include <stdio.h>\nint main(void) { puts("firmware ready"); return 0; }\n'
    (directory / "starter" / "main.c").write_text(starter, encoding="utf-8")
    (directory / "reference" / "main.c").write_text(reference, encoding="utf-8")
    checks = """[[checks]]
id = "first-program-output"
name = "Strict compile and exact observable output"
type = "c_program"
sources = ["main.c"]
expected_stdout = "firmware ready\\n"
expected_exit = 0
cflags = ["-std=c11", "-Wall", "-Wextra", "-Wpedantic", "-Werror", "-O0", "-g"]
timeout = 20
required = true"""
    return checks, f"```c\n{reference}```"


def _write_unit_test_lab(directory: Path, mission: MissionDef) -> tuple[str, str]:
    (directory / "checks").mkdir(parents=True, exist_ok=True)
    header = '#ifndef MEDIAN3_H\n#define MEDIAN3_H\n#include <stdint.h>\nint16_t median3(int16_t a, int16_t b, int16_t c);\n#endif\n'
    starter_test = '#include "task.h"\nint main(void) { return 0; /* add assertions that kill the defect */ }\n'
    reference_test = '#include "task.h"\n#include <assert.h>\nint main(void){assert(median3(3,1,2)==2);assert(median3(-1,-3,-2)==-2);assert(median3(5,5,1)==5);return 0;}\n'
    for area, test in (("starter", starter_test), ("reference", reference_test)):
        (directory / area / "task.h").write_text(header, encoding="utf-8")
        (directory / area / "test.c").write_text(test, encoding="utf-8")
    good = '#include "task.h"\nint16_t median3(int16_t a,int16_t b,int16_t c){if(a>b){int16_t t=a;a=b;b=t;}if(b>c){int16_t t=b;b=c;c=t;}if(a>b){int16_t t=a;a=b;b=t;}return b;}\n'
    bad = '#include "task.h"\nint16_t median3(int16_t a,int16_t b,int16_t c){(void)b;(void)c;return a;}\n'
    (directory / "checks" / "good_module.c").write_text(good, encoding="utf-8")
    (directory / "checks" / "defective_module.c").write_text(bad, encoding="utf-8")
    checks = """[[checks]]
id = "learner-tests-kill-defect"
name = "Tests accept the good module and reject the defect"
type = "c_test_pair"
test_sources = ["test.c"]
good_source = "checks/good_module.c"
defective_source = "checks/defective_module.c"
cflags = ["-std=c11", "-Wall", "-Wextra", "-Wpedantic", "-Werror", "-O0", "-g"]
timeout = 20
required = true"""
    return checks, f"```c\n{reference_test}```"


def _write_board_checkpoint(directory: Path, mission: MissionDef) -> tuple[str, str]:
    (directory / "checks").mkdir(parents=True, exist_ok=True)
    starter_report = "NUCLEO-C031C6 target build\nTODO: paste build command, ELF machine line, and size output.\n"
    reference_report = "NUCLEO-C031C6 target build FORMAT EXAMPLE\nBuild command: make all STM32CUBE_C0=/path/to/STM32CubeC0\nELF: build/nucleo-c031c6.elf\nMachine: ARM\n"
    starter_evidence = {"board": "NUCLEO-C031C6", "build_command": "", "elf_machine": "", "flash_tool": "", "led_toggled": False, "uart_observed": False, "notes": ""}
    reference_evidence = {"board": "NUCLEO-C031C6 FORMAT EXAMPLE", "build_command": "make all", "elf_machine": "ARM", "flash_tool": "STM32CubeProgrammer", "led_toggled": True, "uart_observed": True, "notes": "Replace this format example with observations from your own connected board."}
    for area, report, evidence in (("starter", starter_report, starter_evidence), ("reference", reference_report, reference_evidence)):
        (directory / area / "build-report.txt").write_text(report, encoding="utf-8")
        (directory / area / "hardware-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    harness = """from pathlib import Path
import sys
report = (Path(sys.argv[1]) / 'build-report.txt').read_text()
required = ('NUCLEO-C031C6', 'Build command:', 'ELF:', 'Machine: ARM')
missing = [item for item in required if item not in report]
if missing:
    print('build report missing: ' + ', '.join(missing), file=sys.stderr)
    raise SystemExit(1)
print('structured ARM build report recorded')
"""
    (directory / "checks" / "verify_build_report.py").write_text(harness, encoding="utf-8")
    checks = """[[checks]]
id = "arm-build-report"
name = "Structured evidence from the genuine ARM target build"
type = "project_harness"
harness = "checks/verify_build_report.py"
timeout = 20
required = true

[[checks]]
id = "physical-board-self-attestation"
name = "Explicit learner-recorded board observations"
type = "manual_evidence"
path = "hardware-evidence.json"
required_fields = ["board", "build_command", "elf_machine", "flash_tool", "led_toggled", "uart_observed", "notes"]
required = true"""
    return checks, f"```json\n{json.dumps(reference_evidence, indent=2)}\n```"


def _mission_files(mission: MissionDef) -> tuple[str, str]:
    if mission.id == "first-build":
        return "`main.c`", "Compile a complete program and match its required output and exit status exactly."
    if mission.id == "unit-testing":
        return "`test.c` and the supplied `task.h`", "Write tests that accept the correct implementation and expose the supplied defect."
    if mission.id == "packaging":
        return "`rq.c`, `rq.h`, `Makefile`, and `CMakeLists.txt`", "Build, install, and consume the library successfully with both Make and CMake."
    if mission.id == "consumer-integration-release":
        return "`consumer.c`", "Compile, link, and run a consumer using only the installed public header and static archive."
    if mission.id == "stm32-board-checkpoint":
        return "`build-report.txt` and `hardware-evidence.json`", "Build a real ARM ELF, flash explicitly, and record what you actually observed on your board."
    return "`task.c` (keep the public declarations in `task.h` unchanged)", "Implement the declared C interface so every normal, boundary, and invalid case in the immutable harness passes."


def _parameter_notes(declarations: str) -> str:
    notes: list[str] = []
    functions = re.findall(
        r"([A-Za-z_][A-Za-z0-9_\s*]+?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^;{}]*)\)\s*;",
        declarations,
    )
    for return_type, function_name, parameters in functions:
        for raw in parameters.split(","):
            parameter = raw.strip()
            if not parameter or parameter == "void":
                continue
            names = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", parameter)
            if not names:
                continue
            name = names[-1]
            if name.startswith("out_") or name.startswith("result"):
                meaning = "caller-owned destination written only when the operation succeeds"
            elif name in {"count", "length", "size", "capacity"} or name.endswith("_count"):
                meaning = "number of elements or bytes available; zero is a boundary case"
            elif name == "context":
                meaning = "opaque state owned by the caller; its lifetime must cover the call"
            elif "*" in parameter and "const" in parameter:
                meaning = "read-only input accessed through a pointer; null handling follows the contract"
            elif "*" in parameter:
                meaning = "pointer to caller-owned state that the function may update"
            elif "bool" in parameter:
                meaning = "a true/false input flag"
            else:
                meaning = "an input value; its meaningful range is demonstrated below"
            notes.append(f"- `{name}` from `{parameter}`: {meaning}.")
        clean_return = " ".join(return_type.split())
        if "bool" in clean_return:
            return_meaning = "returns `true` on success and `false` when the operation is rejected"
        elif "enum" in clean_return:
            return_meaning = "returns one of the named status or state values declared above"
        elif clean_return == "void":
            return_meaning = "returns no value; the observable result is a state change"
        else:
            return_meaning = "returns the result or status defined by the required behavior"
        notes.append(f"- `{function_name}` return type `{clean_return}`: {return_meaning}.")
    return "\n".join(notes) or "The concrete calls below define every accepted value and observable result."


def _sublevel_summary(mission: MissionDef) -> str:
    special = {
        "workstation-orientation": (
            "Define `firmware_status` in `task.c`; the supplied driver checks zero, one, "
            "and larger unsigned boot counts."
        ),
        "first-build": (
            "Edit the supplied `main` so the program prints exactly `firmware ready` with "
            "a newline and exits successfully."
        ),
        "unit-testing": (
            "Write C assertions that accept a correct `median3` module and expose a deliberately defective one."
        ),
        "packaging": (
            "Repair, build, install, and relocate a static record-queue library with Make and CMake."
        ),
        "consumer-integration-release": (
            "Prove a clean consumer can compile and link only against the installed record-queue package."
        ),
        "stm32-board-checkpoint": (
            "Build the ARM target and record only the NUCLEO-C031C6 flash, LED, and UART evidence you observe."
        ),
    }
    if mission.id in special:
        return special[mission.id]
    spec = EXERCISES.get(mission.id)
    if spec is None:
        return mission.assignment
    names = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*;", spec.declarations)
    subject = ", ".join(f"`{name}`" for name in names) or "the declared C interface"
    return f"Implement {subject}: {spec.contract}"


def _briefing(mission: MissionDef, spec: Exercise | None, assessed: str, contract: str) -> str:
    files, success = _mission_files(mission)
    if mission.id == "workstation-orientation":
        explanation = """This sublevel teaches the simplest firmware-style status contract. `boot_count` is an unsigned count of successful boots already observed. An unsigned value cannot be negative. The `U` suffix in `0U`, `1U`, and `42U` tells C that each literal is unsigned.

You are **not** writing a complete program and must **not** create `main`. The trusted test and visible-run harnesses provide `main` for you. Your entire coding job is to define the function already declared in `task.h`."""
        wrong = """`task.c` contains only a comment, so `firmware_status` has been declared but not defined. Add its definition there. The function currently cannot be linked or called at all."""
        examples = """- `firmware_status(0U)` must return `-1`: zero means the firmware has not recorded a successful boot.
- `firmware_status(1U)` must return `0`: one successful boot is enough.
- `firmware_status(42U)` must return `0`: every positive boot count represents success.

The return value is a status, not the number of boots. Here, zero means success and `-1` means the required boot has not happened."""
        why = """A firmware module often reports readiness with a small status function that another module calls during boot. If zero and nonzero counts are confused, later initialization may run before the system has ever booted successfully. This small contract teaches declaration versus definition, unsigned input, and status returns before adding a complete program."""
    elif mission.id == "first-build":
        explanation = """This is a complete C program, so you **do** edit the supplied `main` function in `main.c`. `main` is where a hosted C program begins. `puts` writes text and automatically adds a newline. Returning zero from `main` tells the terminal that the program succeeded."""
        wrong = """The starter prints `firmware pending` and returns `1`, so both observable results violate the assignment. Change the string to exactly `firmware ready` and return `0`."""
        examples = """- Standard output must contain exactly `firmware ready` followed by one newline.
- The process exit status must be `0`.
- Extra spaces, extra lines, different capitalization, or returning `1` are failures because another tool may consume this exact interface."""
        why = """Command-line build tools and automated firmware pipelines observe both output bytes and process status. This exercise makes those two interfaces visible: the newline is part of stdout, and zero from `main` is the operating system's success signal."""
    elif mission.id == "compiler-warnings":
        explanation = """The function converts a raw reading from a 12-bit ADC into millivolts. A 12-bit ADC code can be **0 through 4095**. `reference_mv` is the voltage, in millivolts, represented by the maximum code. The calculation is approximately:

```text
millivolts = code * reference_mv / 4095
```

The starter looks close, but embedded C arithmetic happens in fixed-width integer types. You must validate the inputs and make the multiplication happen as `uint32_t` arithmetic so the intermediate result cannot wrap before division."""
        wrong = """The starter checks only whether `out_mv` is null. It does not reject an impossible ADC code above 4095 or a zero reference voltage. It also performs the multiplication without explicitly widening an operand first."""
        examples = """- `code = 0`, `reference_mv = 3300` → return `true` and store `0` in `*out_mv`.
- `code = 4095`, `reference_mv = 3300` → return `true` and store `3300`.
- `code = 4096` → return `false` because it is outside a 12-bit ADC's range.
- `reference_mv = 0` → return `false`.
- `out_mv = NULL` → return `false`; there is nowhere safe to store the answer.

On every failure, the function must not write through `out_mv`. A successful calculation should use a `uint32_t` intermediate before narrowing the final, known-to-fit result to `uint16_t`."""
        why = """ADC conversion code sits directly between electrical measurements and control decisions. An unnoticed narrowing or invalid raw code can turn into a believable but wrong voltage, so strict conversion warnings and explicit range checks are treated as defects rather than cosmetic messages."""
    elif mission.id == "unit-testing":
        explanation = """You are writing the test program in `test.c`, not implementing `median3`. The engine compiles your tests twice: once with a correct `median3` and once with a deliberately defective version. A useful test suite must accept the correct module and make the defective module fail."""
        wrong = """The starter `main` returns immediately and tests nothing. Add ordinary C assertions that cover different input orders, repeated values, negative values, and limits. Keep the public declaration in `task.h` unchanged."""
        examples = """- `median3(1, 2, 3)` must be `2`, and changing the argument order must not change the median.
- `median3(7, 7, 2)` must be `7`.
- Include negative and limiting `int16_t` values so an implementation that merely returns one fixed argument cannot survive."""
        why = """A test that only runs is not necessarily useful: it must distinguish a correct module from a plausible defect. Firmware regressions often hide at ordering, duplicate-value, sign, and limit boundaries, so this sublevel makes the tests themselves the C artifact you design."""
    elif mission.id == "packaging":
        explanation = """This is a multi-file build exercise. You are producing a static C library that can be installed into a temporary prefix and used by a consumer that has no path back into the source tree. Both Make and CMake must describe the same public header and archive."""
        wrong = """Inspect `rq.c`, `rq.h`, `Makefile`, and `CMakeLists.txt`. The starter reports the wrong public version or leaves the package/consumer contract incomplete. Repair the supplied files; do not create `task.c` or change the trusted project harness."""
        examples = """- `make ... install PREFIX=<temporary-directory>` must place `rq.h` under `include` and `librq.a` under `lib`.
- A separate program compiled with only that installed prefix must include `<rq.h>`, link the archive, and observe version `1.0.0`.
- A clean CMake configure, build, and install must provide the same result."""
        why = """A reusable library is more than source that builds inside its own directory. Firmware teams need a public header, archive, version, and install layout that another project can consume without private paths. Make and CMake must publish the same boundary."""
    elif mission.id == "consumer-integration-release":
        explanation = """This final battle starts on the other side of a library boundary. The trusted harness creates an installed prefix containing only `include/rq.h` and `lib/librq.a`. Your `consumer.c` must use that public installation as an ordinary external dependency; it cannot include private source or rely on a source-tree path."""
        wrong = """The starter already includes the installed public header, but `main` returns failure without checking the API. Use `rq_version()` and `rq_add()` through that header. Return zero only when the version is exactly `1.0.0` and `rq_add(19, 23)` returns `42`."""
        examples = """- The strict consumer compile must find `<rq.h>` only through the temporary installed include directory.
- The link must resolve calls only from the installed `librq.a`.
- Version `1.0.0` and the result `42` mean success and `main` returns `0`; any mismatch returns a nonzero status."""
        why = """The final proof of a C library is a separate consumer. Building against installed-only paths catches leaked private headers, missing archive symbols, and accidental dependence on the library source tree—problems that unit tests inside the library can miss."""
    elif mission.id == "stm32-board-checkpoint":
        explanation = """This hardware sublevel uses the repository's STM32 project rather than asking for a new `task.c`. Build the ARM ELF first. Flashing is always a separate explicit command. Record only LED and UART behavior you personally observed on the NUCLEO-C031C6."""
        wrong = """The starter evidence files are examples, not claims about your desk. Replace their fields with the build command, ELF information, flash tool, and observations you actually obtained. Never report a flash or LED result that did not happen."""
        examples = """- The build report names the ARM command and identifies the output as an ARM ELF.
- The hardware record names the NUCLEO-C031C6, the confirmed flash tool, and your actual PA5 LED and USART2 observations.
- If hardware is unavailable, leave this sublevel incomplete rather than inventing evidence."""
        why = """Host simulations prove portable logic, but only a target build and explicit flash exercise the real compiler, linker, debug probe, pins, and board wiring. Separating machine-checked build evidence from your physical observations keeps the result honest and reproducible."""
    else:
        explanation = (
            f"Define the interface in `task.c` so this rule holds: {contract} "
            "The caller will use the return value to distinguish success from failure, so handle "
            "invalid inputs deliberately instead of producing a plausible-looking result."
        )
        function_names = (
            re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*;", spec.declarations)
            if spec is not None else []
        )
        subject = ", ".join(f"`{name}`" for name in function_names) or "this code"
        starter_issues = {
            "gdb-first-steps": "The loop condition uses `i <= count`, so it tries to read one element beyond the live array. Change the bound so only indices strictly smaller than `count` are visited.",
            "strings": "The starter calls `strcat` without proving that the destination is terminated or that the suffix and final null byte fit. Replace that unbounded write with the checked contract described below.",
            "undefined-behavior": "The starter dereferences `out_value` and shifts immediately. A null output pointer, shift of 32 or more, or unrepresentable result reaches undefined or unwanted behavior before any validation.",
            "sanitizers": "The loop uses `index <= count`, which reads `values[count]` one element past the array. Sanitizers expose that access; repair the loop bound and preserve the null rules.",
        }
        wrong = starter_issues.get(
            mission.id,
            f"The supplied `task.c` contains a TODO but no definition for {subject}. "
            "Add the missing code there; keep the declarations and trusted drivers unchanged.",
        )
        examples = (
            "The following are executable examples of the required behavior. Read each assertion as "
            "‘this call must make the condition true’:\n\n```c\n" + spec.tests.strip() + "\n```"
            if spec is not None else contract
        )
        why = (
            f"This sublevel turns **{', '.join(mission.concepts)}** into behavior a caller can verify. "
            f"In firmware, a defect in {subject} can corrupt state or hide a hardware failure even when "
            "one ordinary example appears correct."
        )
    if mission.id == "first-build":
        signature = "`main.c` already contains `int main(void)`. Edit that function; do not create a second entry point."
    elif mission.id == "workstation-orientation":
        signature = """```c
int firmware_status(unsigned boot_count);
```

Do not change this declaration.

- `boot_count` is the number of successful boots already observed. Because it is `unsigned`, its range starts at zero; it can never represent a negative count.
- The `int` return value is a status code: `0` means ready, while `-1` means no successful boot has occurred."""
    elif mission.id == "compiler-warnings":
        signature = """```c
bool adc_to_millivolts(uint16_t code, uint16_t reference_mv, uint16_t *out_mv);
```

Do not change this declaration.

- `code` is the raw 12-bit ADC result.
- `reference_mv` is the millivolt value represented by full scale.
- `out_mv` points to the caller's destination and is written only on success.
- The function returns `true` after storing a valid result; otherwise it returns `false`."""
    elif spec is not None:
        signature = (
            f"```c\n{spec.declarations}\n```\n\nDo not change these declarations.\n\n"
            + _parameter_notes(spec.declarations)
        )
    else:
        signature = "This is a multi-file or hardware sublevel; the editable artifacts are named below."
    run_instruction = ""
    if mission.id == "workstation-orientation":
        run_instruction = "`./learn run` compiles your function with the visible driver and prints each call and return value."
    elif spec is not None and mission.id not in {"first-build", "unit-testing"}:
        run_instruction = "Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value."
    elif mission.id == "first-build":
        run_instruction = "`./learn run` compiles and executes `main.c`, showing its output and exit status."
    elif mission.id == "unit-testing":
        run_instruction = "`./learn run` compiles `test.c` against both supplied modules and shows whether your tests distinguish them."
    elif mission.id in {"packaging", "consumer-integration-release", "stm32-board-checkpoint"}:
        action = (
            "execute the trusted Make/CMake build and relocation check"
            if mission.id == "packaging" else
            "build the installed-only fixture, compile your consumer, and run it"
            if mission.id == "consumer-integration-release" else
            "validate the recorded ARM build report and hardware evidence; it never flashes the board"
        )
        run_instruction = f"`./learn run` will {action} without submitting; it prints the real build output and first diagnostic."

    if mission.id == "workstation-orientation":
        boundary = "`boot_count` accepts every value representable by `unsigned`. Zero is the only not-ready value; one and every larger unsigned value are ready. There are no pointer, text, or negative inputs in this interface."
        failure = "There is no invalid value in the `unsigned` input range. Reporting not-ready is an ordinary status result, not a crash or compile failure, and the function must have no side effects."
    elif mission.id == "first-build":
        boundary = "`main(void)` takes no input. The output comparison is byte-for-byte: capitalization, spaces, the single newline, additional text, and exit status are all observable boundaries."
        failure = "If either observable result is wrong, the checker reports the actual output or exit status and rejects the submission. A compiler warning also fails the strict build."
    elif mission.id == "unit-testing":
        boundary = "Your tests must cover input order, repeated values, negative values, and `int16_t` limits. They must not depend on one particular correct implementation."
        failure = "The test executable must return zero for the good module and fail for the defective module. A suite that rejects both—or accepts both—does not pass."
    elif mission.id == "packaging":
        boundary = "The package boundary is the install prefix: only `include/rq.h` and `lib/librq.a` may be visible to the relocated consumer. Both clean Make and clean CMake builds must work."
        failure = "A compile, archive, install, link, version, or relocated execution error returns nonzero and prints the real failing command's output. No source-tree include fallback is accepted."
    elif mission.id == "consumer-integration-release":
        boundary = "The consumer receives no source-tree files—only the installed header and archive. It must check both a no-argument version result and `rq_add` with the concrete inputs 19 and 23."
        failure = "Return a nonzero value if the version or arithmetic result differs. A missing public declaration or symbol must fail naturally at compile or link time."
    elif mission.id == "stm32-board-checkpoint":
        boundary = "Build evidence must identify a real ARM ELF. Hardware fields describe only the named NUCLEO-C031C6 and only observations made after an explicit flash. Missing hardware is allowed to leave the sublevel unfinished."
        failure = "A missing tool or disconnected board is reported as unavailable evidence, never converted into a successful observation. Ordinary `run`, `test`, and repository validation never flash hardware."
    elif mission.id == "compiler-warnings":
        failure = "Reject a code above 4095, a zero reference voltage, or a null output pointer by returning `false`. Check all three before writing through `out_mv`, so a failed call cannot overwrite the caller's previous value. Accepted inputs return `true` only after the complete millivolt result has been stored."
    else:
        declaration = spec.declarations if spec is not None else ""
        boundary_parts = [
            "The executable calls above define the ordinary values and the first accepted or rejected boundaries for this exact interface."
        ]
        if "*" in declaration:
            boundary_parts.append("For every pointer parameter, follow the shown null rule before dereferencing; caller-owned output is committed only on success.")
        if re.search(r"\b(count|length|capacity|size)\b", declaration):
            boundary_parts.append("A zero extent and the first extent beyond available storage are distinct cases; never access an index unless it is strictly inside the validated extent.")
        boundary_parts.append(f"The required invariant is: {contract}")
        boundary = " ".join(boundary_parts)
        if "bool " in declaration:
            failure = "Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete."
        elif "enum " in declaration:
            failure = "Return the named failure or safe-state enumerator for rejected work; never invent an out-of-range enum result or partially publish output."
        else:
            failure = "Produce exactly the documented value for every accepted input. Any rejected operation must use its documented status without undefined behavior or a partial state update."

    if mission.id in {"packaging", "consumer-integration-release", "stm32-board-checkpoint"}:
        forbidden = "Do not edit anything below `curriculum/` or the trusted checker files."
    elif mission.id == "first-build":
        forbidden = "Do not create a second `main` or edit anything below `curriculum/`."
    else:
        forbidden = "Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers."
    return f"""# {mission.title}

## Your task

{explanation}

Edit {files} in the attempt directory printed by `./learn status`. {forbidden} {run_instruction} Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

{why}

{wrong}

## Read the function signature

{signature}

## Concrete examples

{examples}

## Expected failure behavior

{failure}
"""


def _lesson(mission: MissionDef, exercise_spec: Exercise | None) -> str:
    files, success = _mission_files(mission)
    contract = exercise_spec.contract if exercise_spec is not None else CASE_FACTS.get(mission.id, mission.assignment)
    if mission.id == "first-build":
        contract = "Your program must print exactly `firmware ready` followed by a newline, then return exit status zero."
    interface = ""
    if exercise_spec is not None and mission.id not in {"workstation-orientation", "first-build", "unit-testing"}:
        interface = f"""
## Interface you must preserve

```c
{exercise_spec.declarations}
```
"""
    return f"""# {mission.title}

## What you are doing

{mission.assignment} In this version of the exercise you learn by changing and running real C artifacts; there is no reflection or essay to submit.

## Why firmware engineers care

The key ideas are **{', '.join(mission.concepts)}**. Firmware must keep behaving at boundaries and after unusual inputs, not merely in one demonstration. This exercise turns those ideas into behavior the compiler and tests can observe.

## Files you will edit

Edit {files}. Do not edit files below `curriculum/` or the hidden acceptance harness. Your personal copy is inside the attempt workspace printed by `./learn status`.

## Required behavior

{contract}
{interface}
## A practical way to begin

1. Read the complete starter and public interface before changing it.
2. Find the placeholder or deliberate defect and predict the first failing case.
3. Make the smallest correct change while keeping strict compiler warnings enabled.
4. Run `./learn test` and address the first useful diagnostic.
5. Check the zero/empty case, an ordinary case, and the first invalid or maximum case.

## Common mistake

Do not weaken the function signature, compiler flags, error result, or bounds just to make one example work. A passing implementation must preserve the contract for callers that you cannot see.

## Success looks like

{success} Run `./learn test`; every required check must report `PASS`. Use `./learn solution` whenever you need the worked implementation—solutions carry no penalty.
"""


def _replace_check(manifest: Path, check: str) -> None:
    original = manifest.read_text(encoding="utf-8")
    prefix = original.split("[[checks]]", 1)[0].rstrip()
    manifest.write_text(prefix + "\n\n" + check.strip() + "\n", encoding="utf-8")


def _clear_generated_files(directory: Path) -> None:
    for area in ("starter", "reference"):
        root = directory / area
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
    checks = directory / "checks"
    if checks.exists():
        shutil.rmtree(checks)


def _write_level_catalog() -> None:
    curriculum_root = Path(
        os.environ.get("LEARN_C_CURRICULUM_ROOT", str(curriculum_source.CURRICULUM))
    ).resolve()
    manifest_lines = ["schema_version = 1", ""]
    for stage_number in sorted(curriculum_source.STAGE_NAMES):
        missions = [mission for mission in MISSIONS if mission.stage == stage_number]
        if len(missions) < 5:
            raise RuntimeError(f"level {stage_number} needs at least five distinct sublevels")
        level_id, objective = LEVEL_DETAILS[stage_number]
        title = curriculum_source.STAGE_NAMES[stage_number]
        stage_directory = _mission_directory(missions[0].id).parent
        overview = stage_directory / "LEVEL.md"
        overview_relative = overview.relative_to(curriculum_root).as_posix()
        outcomes = list(LEVEL_OUTCOMES[stage_number])
        sublevel_lines = []
        for index, mission in enumerate(missions, 1):
            suffix = " — FINAL BATTLE" if mission is missions[-1] else ""
            sublevel_lines.append(
                f"{index}. **{mission.title}** (`{mission.id}`){suffix} — {_sublevel_summary(mission)}"
            )
        final_integrates = FINAL_INTEGRATES[stage_number]
        topic_practice = TOPIC_PRACTICE[stage_number]
        mission_by_id = {mission.id: mission for mission in missions}
        if set().union(*(set(ids) for ids in topic_practice.values())) != set(mission_by_id):
            raise RuntimeError(f"level {stage_number} practice clusters must cover every sublevel")
        practice_lines = [
            f"- **{topic}** is practised in: "
            + ", ".join(
                mission_by_id[practice_id].title
                for practice_id in practice_ids
            )
            for topic, practice_ids in topic_practice.items()
        ]
        overview.write_text(
            f"# Level {stage_number}: {title}\n\n"
            f"## Main objective\n\n{objective}\n\n"
            "## What you should know before starting\n\n"
            + ("No C knowledge is assumed. You only need a terminal and text editor.\n\n" if stage_number == 1 else
               f"Complete Level {stage_number - 1}; this level builds directly on its C contracts and debugging habits.\n\n")
            + "## Why these concepts belong together\n\n"
            f"These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **{missions[-1].title}**.\n\n"
            "## What you will build and learn\n\n"
            + "\n".join(f"- {item}" for item in outcomes) + "\n\n"
            "## Ordered sublevels\n\n" + "\n".join(sublevel_lines) + "\n\n"
            "## Topic practice coverage\n\n"
            "Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.\n\n"
            + "\n".join(practice_lines) + "\n\n"
            "## Final battle\n\n"
            f"**{missions[-1].title}** is the last required sublevel. It integrates **"
            + "**, **".join(next(item.title for item in missions if item.id == value) for value in final_integrates)
            + "**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.\n",
            encoding="utf-8",
        )
        sublevel_ids = [mission.id for mission in missions]
        manifest_lines.extend([
            "[[levels]]",
            f"id = {json.dumps(level_id)}",
            f"title = {json.dumps(title)}",
            f"order = {stage_number}",
            f"objective = {json.dumps(objective)}",
            f"learning_outcomes = {json.dumps(outcomes)}",
            f"overview = {json.dumps(overview_relative)}",
            f"sublevels = {json.dumps(sublevel_ids)}",
            f"final_battle = {json.dumps(missions[-1].id)}",
            f"final_integrates = {json.dumps(final_integrates)}",
            "topic_practice = [",
            *(
                f"  {{ topic = {json.dumps(topic)}, sublevels = {json.dumps(practice)} }},"
                for topic, practice in topic_practice.items()
            ),
            "]",
            "",
        ])
    (curriculum_root / "levels.toml").write_text(
        "\n".join(manifest_lines), encoding="utf-8"
    )


def enhance_curriculum() -> None:
    schema_directory = Path(
        os.environ.get("LEARN_C_CURRICULUM_ROOT", str(curriculum_source.CURRICULUM))
    ).resolve() / "schema-example"
    schema_directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        Path(__file__).resolve().parent / "templates" / "level.toml.example",
        schema_directory / "level.toml.example",
    )
    for mission in MISSIONS:
        directory = _mission_directory(mission.id)
        _clear_generated_files(directory)
        manifest = directory / "level.toml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace('version = "1.0.0"', 'version = "2.0.0"', 1),
            encoding="utf-8",
        )
        spec = EXERCISES.get(mission.id)
        if mission.id == "first-build":
            checks, solution_artifact = _write_first_program(directory, mission)
            _replace_check(directory / "level.toml", checks)
            assessed = "Edit `main.c` so it prints the exact required status line and returns success. No reflection is required."
        elif mission.id == "unit-testing":
            checks, solution_artifact = _write_unit_test_lab(directory, mission)
            _replace_check(directory / "level.toml", checks)
            assessed = "Write `test.c` so it accepts the correct module and exposes the supplied defect."
        elif mission.id == "packaging":
            checks, solution_artifact = _write_packaging_project(directory, mission)
            _replace_check(directory / "level.toml", checks)
            assessed = "Repair and package the supplied library with both Make and CMake, install it into temporary prefixes, and run a relocated consumer."
        elif mission.id == "consumer-integration-release":
            checks, solution_artifact = _write_consumer_project(directory, mission)
            _replace_check(directory / "level.toml", checks)
            assessed = "Complete `consumer.c` so it verifies and uses a library strictly through its installed public header and archive."
        elif mission.id == "stm32-board-checkpoint":
            checks, solution_artifact = _write_board_checkpoint(directory, mission)
            _replace_check(directory / "level.toml", checks)
            assessed = "Run the pinned ARM target build, then explicitly flash your connected board and replace the format example with your own LED/UART observations. Physical observations are self-attested, never simulated by the checker."
        elif spec is not None:
            (directory / "checks").mkdir(parents=True)
            header = _header(mission, spec.declarations)
            reference_source = f"/* Mission: {mission.title} */\n" + _source(spec.implementation)
            starter_source = spec.starter or (
                '#include "task.h"\n\n'
                f'/* TODO — {mission.title}: implement the declared interface.\n'
                f' * Contract to prove: {spec.contract}\n */\n'
            )
            for area in ("starter", "reference"):
                (directory / area / "task.h").write_text(header, encoding="utf-8")
            (directory / "starter" / "task.c").write_text(starter_source.rstrip() + "\n", encoding="utf-8")
            (directory / "reference" / "task.c").write_text(reference_source, encoding="utf-8")
            harness_id = (
                mission.id if mission.id in DISTINCT_ALIAS_EXERCISES
                else PRACTICAL_ALIASES.get(mission.id, mission.id)
            )
            (directory / "checks" / "test.c").write_text(_harness(harness_id, spec.tests), encoding="utf-8")
            (directory / "checks" / "visible.c").write_text(
                _visible_harness(harness_id, spec.declarations, spec.tests), encoding="utf-8"
            )
            flags = ", ".join(json.dumps(flag) for flag in spec.flags)
            sim_config = ""
            support_id = (
                mission.id if mission.id in DISTINCT_ALIAS_EXERCISES
                else PRACTICAL_ALIASES.get(mission.id, mission.id)
            )
            if support_id in SIM_SUPPORT:
                sources, _, _, _ = SIM_SUPPORT[support_id]
                sim_config = (
                    f"\nsupport_sources = {json.dumps(list(sources))}"
                    "\nsupport_include_dirs = [\"platforms/host/include\"]"
                )
            checks = f"""[[checks]]
id = "immutable-c-contract"
name = "Strict build and immutable behavior tests"
type = "c_harness"
sources = ["task.c"]
harness = "checks/test.c"
cflags = [{flags}]
timeout = 20
required = true{sim_config}"""
            _replace_check(directory / "level.toml", checks)
            solution_artifact = f"```c\n{reference_source}```"
            assessed = f"Implement the `task.h` contract in `task.c`: {spec.contract}"
            if mission.id == "gdb-debugging":
                transcript = """# Supplied GDB transcript
(gdb) break replace_value
(gdb) run
(gdb) watch values[3]
Old value = 17
New value = -1
(gdb) bt
#0 replace_value (values=0x..., count=3, target=17, replacement=-1) at faulty.c:8
#1 main () at reproduce.c:12
Diagnosis: the loop used index <= count and wrote values[3], one element past the array.
"""
                faulty = '#include <stddef.h>\n#include <stdint.h>\nsize_t replace_value(int32_t *v,size_t n,int32_t t,int32_t r){size_t hits=0;for(size_t i=0;i<=n;++i)if(v[i]==t){v[i]=r;++hits;}return hits;}\n'
                for area in ("starter", "reference"):
                    (directory / area / "gdb-transcript.txt").write_text(transcript, encoding="utf-8")
                    (directory / area / "faulty.c").write_text(faulty, encoding="utf-8")
        else:
            raise RuntimeError(f"mission {mission.id} has no practical exercise")

        contract = (
            "print exactly 'firmware ready' plus a newline and return zero"
            if mission.id == "first-build" else
            ("compile and run a consumer using only the installed rq.h and librq.a, returning zero after verifying version 1.0.0 and rq_add(19, 23) == 42"
             if mission.id == "consumer-integration-release" else
            (spec.contract if spec is not None else mission.assignment)
            )
        )
        (directory / "lesson.md").write_text(_lesson(mission, spec), encoding="utf-8")
        if mission.id == "stm32-board-checkpoint":
            lesson_path = directory / "lesson.md"
            lesson_path.write_text(
                lesson_path.read_text(encoding="utf-8").replace(
                    "Write `answer.md` with the exact sections Prediction, Evidence, Decision, and Boundary Cases. The checker verifies structure and substance, not a secret phrase. Your reasoning remains yours: the model solution demonstrates one defensible answer, while a different conclusion is acceptable when its evidence and boundary treatment support it.",
                    "Use `platforms/stm32c031/target_project` for the real ARM compile/link. Record its command, ELF machine, and size in `build-report.txt`; after an explicit confirmed flash, record your own LED and UART observations in `hardware-evidence.json`. The engine validates structure and labels the observation as self-attested because software cannot prove what happened on your desk."
                ),
                encoding="utf-8",
            )
        (directory / "briefing.md").write_text(
            _briefing(mission, spec, assessed, contract), encoding="utf-8"
        )
        (directory / "solution.md").write_text(
            f"# Full solution: {mission.title}\n\n"
            f"This worked implementation demonstrates {', '.join(mission.concepts)}. "
            "Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.\n\n"
            f"{solution_artifact}\n",
            encoding="utf-8",
        )
        focus = spec.contract if spec is not None else CASE_FACTS.get(mission.id, mission.assignment)
        hints = (
            f"# Hint 1 — Contract for {mission.title}\n\n{focus}\n",
            f"# Hint 2 — Boundary for {mission.title}\n\nExercise zero or empty input, one ordinary value, the largest valid value, and the first invalid value. Check that failure does not partially modify caller-owned output.\n",
            f"# Hint 3 — Concrete route for {mission.title}\n\nKeep the assessed interface fixed and use {mission.concepts[-1]} to interpret the first compiler or checker diagnostic. Rerun `./learn test` after one focused change. The full worked implementation remains available through `./learn solution`.\n",
        )
        for index, content in enumerate(hints, 1):
            (directory / "hints" / f"{index:02d}.md").write_text(content, encoding="utf-8")
    _write_level_catalog()


def main() -> int:
    enhance_curriculum()
    print(f"Enhanced {len(MISSIONS)} missions; {len(EXERCISES)} use immutable C harnesses.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
