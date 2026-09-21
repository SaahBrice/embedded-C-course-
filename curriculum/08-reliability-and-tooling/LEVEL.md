# Level 8: Reliability and Tooling

## Main objective

Find and prevent defects with tests, debuggers, sanitizers, static analysis, safe arithmetic, concurrency rules, and secure parsing.

## What you should know before starting

Complete Level 7; this level builds directly on its C contracts and debugging habits.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Incident: Intermittent Logger Reset**.

## What you will build and learn

- Write tests that expose defects and use debugger, sanitizer, and analyzer evidence
- Prevent overflow, races, undefined behavior, and unsafe parsing
- Repair an intermittent logger-reset incident from reproducible evidence

## Ordered sublevels

1. **Test C Modules in Isolation** (`unit-testing`) — Write C assertions that accept a correct `median3` module and expose a deliberately defective one.
2. **Test Collaborating Modules** (`integration-testing`) — Implement `bool`, `bool`, `logger_cycle`: Deterministic fakes expose call count and transferred value, including read and storage failure branches between collaborating modules.
3. **Diagnose a Firmware Fault with GDB** (`gdb-debugging`) — Implement `replace_value`: The repaired loop touches exactly the live array range; a watchpoint would show only matching elements being changed.
4. **Use Host Sanitizers** (`sanitizers`) — Implement `copy_samples`: The sanitizer-backed build verifies that byte count derives from a validated element count and no zero-length call dereferences null.
5. **Act on Static Analysis** (`static-analysis`) — Implement `checked_array_read`: Null and bounds findings are repaired with executable checks before the array access occurs.
6. **Harden Arithmetic** (`integer-overflow`) — Implement `checked_scale`: `checked_scale` performs multiplication in a wider defined type and narrows only after both signed limits are proven.
7. **Reason About Shared State** (`concurrency`) — Implement `sequence_is_newer`: Single-word sequence snapshots are ordered with defined unsigned wraparound and an explicit half-range rule.
8. **Validate Untrusted Data** (`secure-c`) — Implement `frame_payload_length`: The received extent is validated before trusting an attacker-controlled payload length or publishing it.
9. **Incident: Intermittent Logger Reset** (`incident-response-release`) — FINAL BATTLE — Implement `watchdog_elapsed`, `ring_indices_valid`, `recovery_required`: The incident-response release reproduces wraparound timeout behavior, checks a persisted ring invariant, and makes one explicit recovery decision from independent fault evidence.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **executable defect evidence** is practised in: Test C Modules in Isolation, Test Collaborating Modules, Diagnose a Firmware Fault with GDB, Use Host Sanitizers, Act on Static Analysis, Incident: Intermittent Logger Reset
- **undefined behavior and data integrity** is practised in: Use Host Sanitizers, Act on Static Analysis, Harden Arithmetic, Reason About Shared State, Validate Untrusted Data, Incident: Intermittent Logger Reset
- **regression and recovery reasoning** is practised in: Test C Modules in Isolation, Test Collaborating Modules, Diagnose a Firmware Fault with GDB, Reason About Shared State, Validate Untrusted Data, Incident: Intermittent Logger Reset

## Final battle

**Incident: Intermittent Logger Reset** is the last required sublevel. It integrates **Act on Static Analysis**, **Harden Arithmetic**, **Reason About Shared State**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
