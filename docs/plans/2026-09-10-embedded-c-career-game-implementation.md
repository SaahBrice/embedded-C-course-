# Embedded C Career Game Implementation Plan

> **For agentic workers:** Use the host's available task-by-task implementation workflow. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, tested terminal engineering-career game that teaches C from first compilation through embedded firmware, reusable libraries, STM32 practice, and a sensor data-logger capstone.

**Architecture:** A dependency-free Python package powers the `./learn` terminal command, discovers versioned TOML mission packages, creates isolated attempts, executes bounded checker plugins, and persists progress atomically. Curriculum packages contain Markdown instruction, starter projects, hints, model solutions, and declarative checks; host simulations and STM32 material remain separated behind narrow interfaces.

**Tech Stack:** Python 3.11+ standard library, C11/C17, GCC or Clang, Make, CMake for the library/capstone stages, GDB guidance, host sanitizers where available, CMSIS/STM32Cube command-line guidance for the Nucleo-C031C6, `unittest` for the engine, and shell-based end-to-end checks.

## Global Constraints

- The main campaign unlocks missions strictly in order; completed missions can be replayed without changing earlier attempts.
- All lessons, hints, explanations, and reference solutions are freely accessible.
- Activities include prediction, tracing, writing from scratch, debugging, refactoring, review, datasheet work, API design, simulation, and integration—not only completing starter code.
- Normal missions target 45–60 minutes; projects may span sessions.
- Stable mission IDs and explicit prerequisites allow intermediary missions to be inserted without renaming existing content.
- Host testing is the default. Hardware build and flashing are explicit and never triggered by ordinary test or submit commands.
- Portable logic remains independent from STM32-specific code.
- Progress and attempts survive interruption through atomic writes and immutable curriculum sources.
- A broken mission, unavailable tool, learner compilation failure, failed check, timeout, and hardware failure must be reported as distinct conditions.
- The completed course covers all eleven curriculum stages in the approved design and ends with reusable libraries plus a sensor data-logger capstone.

## Observable command decisions

- `./learn` with no arguments prints help and exits 0.
- Successful commands exit 0; learner check failures and locked/unknown mission requests exit 1; engine/configuration failures exit 2.
- Human-readable command results go to standard output; actionable errors go to standard error.
- `start` resumes the open attempt for the current mission unless `--new` is supplied. `replay` always creates a fresh numbered attempt.
- `solution` displays content without mutating completion state. `submit` is the only command that unlocks the successor.
- `reset` requires both an explicit attempt ID and `--yes`; it removes only that working attempt and never completion history.
- Progress is local to the repository under `.learn/progress.json`; generated attempts live under `.learn/attempts/`. These paths are excluded from version control.
- Check commands have a 10-second default timeout, overridable per mission up to 120 seconds. Timeouts terminate the child process group and fail the check.
- No Git repository will be initialized or commits created unless the user separately requests it.

---

### Task 1: Package model, discovery, and validation

**Files:**
- Create: `learn_engine/__init__.py`
- Create: `learn_engine/models.py`
- Create: `learn_engine/catalog.py`
- Create: `learn_engine/errors.py`
- Create: `tests/test_catalog.py`
- Create: `pyproject.toml`

**Interfaces:**
- Produces: `Mission.from_manifest(path: Path) -> Mission`
- Produces: `Catalog.load(root: Path) -> Catalog`
- Produces: `Catalog.ordered_missions() -> tuple[Mission, ...]`
- Produces: `Catalog.validate() -> list[ValidationIssue]`

- [ ] Add tests for valid discovery, stable ID/order separation, duplicate IDs/orders, missing files, invalid prerequisites, cycles, first-mission rules, and insertion between existing orders.
- [ ] Verify tests fail because the package model does not exist.
- [ ] Implement frozen mission/checker models, strict supported manifest keys, TOML parsing, deterministic order, prerequisite validation, and cycle detection.
- [ ] Verify `python3 -m unittest tests.test_catalog -v` passes.
- [ ] Run `python3 -m unittest discover -s tests -v` and retain a green baseline.

### Task 2: Atomic progress and isolated attempts

**Files:**
- Create: `learn_engine/progress.py`
- Create: `learn_engine/attempts.py`
- Create: `tests/test_progress.py`
- Create: `tests/test_attempts.py`
- Create: `.gitignore`

**Interfaces:**
- Produces: `ProgressStore.load() -> Progress`
- Produces: `ProgressStore.complete(mission_id, version, attempt_id) -> None`
- Produces: `AttemptStore.start(mission, force_new=False) -> Attempt`
- Produces: `AttemptStore.replay(mission) -> Attempt`
- Produces: `AttemptStore.reset(attempt_id, confirmed=False) -> None`

- [ ] Add tests for empty state, atomic save, corrupt progress, versioned completion, resume, fresh replay, source immutability, path traversal rejection, and confirmed reset scope.
- [ ] Verify focused tests fail for missing stores.
- [ ] Implement JSON persistence using temporary-file replacement and attempt creation using validated repository-relative paths.
- [ ] Verify both focused modules pass.
- [ ] Run the full unit suite.

### Task 3: Bounded checker plugins and diagnostics

**Files:**
- Create: `learn_engine/checkers/__init__.py`
- Create: `learn_engine/checkers/base.py`
- Create: `learn_engine/checkers/command.py`
- Create: `learn_engine/checkers/files.py`
- Create: `learn_engine/checkers/text.py`
- Create: `learn_engine/runner.py`
- Create: `tests/test_checkers.py`
- Create: `tests/fixtures/fake_compiler.py`

**Interfaces:**
- Produces: `CheckerRegistry.run(check_spec, attempt, timeout) -> CheckResult`
- Produces: `MissionRunner.test(attempt) -> MissionResult`
- `CheckResult` distinguishes pass, learner failure, timeout, missing tool, and engine/configuration failure while preserving stdout/stderr.

- [ ] Add tests for file existence, exact/regex text, command success/failure, missing executable, timeout/process cleanup, working-directory isolation, output capture, and unsupported checker types.
- [ ] Verify focused tests fail.
- [ ] Implement an allow-listed checker registry and subprocess runner without shell interpolation; cap output and terminate process groups on timeout.
- [ ] Verify checker tests and then the complete suite pass.

### Task 4: Terminal game interface

**Files:**
- Create: `learn_engine/cli.py`
- Create: `learn_engine/render.py`
- Create: `learn_engine/__main__.py`
- Create: `learn`
- Create: `tests/test_cli.py`

**Interfaces:**
- Produces commands: `map`, `start`, `status`, `lesson`, `test`, `hint`, `solution`, `submit`, `replay`, `reset`, `validate`, and `doctor`.
- Consumes `Catalog`, `ProgressStore`, `AttemptStore`, and `MissionRunner` interfaces defined above.

- [ ] Add CLI tests for help, ordered map, locked access, resume/new attempts, incremental hints, solution display, non-mutating test, gated submit, replay, confirmed reset, exit statuses, stdout/stderr separation, and operation from outside the repository.
- [ ] Verify focused tests fail.
- [ ] Implement `argparse` commands, repository-root resolution from the launcher, readable rendering, and exception-to-exit-code mapping.
- [ ] Verify CLI tests and full unit suite pass.
- [ ] Run a clean end-to-end flow through one fixture mission.

### Task 5: Curriculum authoring system and validator

**Files:**
- Create: `learn_engine/authoring.py`
- Create: `docs/AUTHORING.md`
- Create: `curriculum/schema-example/level.toml.example`
- Create: `tests/test_authoring.py`

**Interfaces:**
- Produces: `CurriculumValidator.validate_all(catalog) -> ValidationReport`
- The `validate` CLI checks required prose, starter safety, check definitions, hint ordering, solution/model-answer presence, reference-solution pass, estimated duration, and platform metadata.

- [ ] Add tests with valid and deliberately broken mission packages covering every diagnostic category.
- [ ] Verify focused tests fail.
- [ ] Implement the validator and authoring documentation with exact manifest fields and extension boundaries.
- [ ] Verify authoring tests and full suite pass.

### Task 6: Stages 1–4 curriculum — toolchain through professional C

**Files:**
- Create: `curriculum/01-orientation/*`
- Create: `curriculum/02-c-foundations/*`
- Create: `curriculum/03-data-memory/*`
- Create: `curriculum/04-professional-c/*`
- Create: `tests/test_curriculum_host.py`

**Interfaces:**
- Adds ordered mission packages using the published manifest/checker contract.
- Provides starter and reference code that builds with `cc -std=c11 -Wall -Wextra -Wpedantic -Werror` unless a mission explicitly studies a diagnostic.

- [ ] Add curriculum tests asserting stage coverage, activity diversity, prerequisite continuity, required educational assets, and passing reference solutions.
- [ ] Verify tests fail with the stages absent.
- [ ] Author guided missions covering compiling/linking, diagnostics, binary/hex, types, expressions, branching, loops, functions, scope, arrays, strings, pointers, storage/lifetime, structs/unions/enums, headers/translation units, preprocessor, defensive APIs, undefined behaviour, and portability.
- [ ] Run all reference checks, curriculum validation, and the unit suite.

### Task 7: Host embedded simulation and stages 5–6

**Files:**
- Create: `platforms/host/include/sim_gpio.h`
- Create: `platforms/host/include/sim_uart.h`
- Create: `platforms/host/include/sim_timer.h`
- Create: `platforms/host/include/sim_adc.h`
- Create: `platforms/host/src/*`
- Create: `platforms/host/tests/*`
- Create: `curriculum/05-embedded-foundations/*`
- Create: `curriculum/06-peripherals/*`
- Create: `tests/test_simulation.py`

**Interfaces:**
- Produces deterministic `sim_gpio_*`, `sim_uart_*`, `sim_timer_*`, and `sim_adc_*` C APIs with resettable state and observable event logs.
- Missions consume these APIs while teaching fixed-width types, masks, qualifiers, register reasoning, GPIO, interrupts, timers, UART, ADC, PWM, SPI, and I2C.

- [ ] Add C harness tests for state transitions, invalid channel/pin handling, deterministic timer ticks, UART buffers, ADC sequences, and event-log reset.
- [ ] Verify simulation tests fail.
- [ ] Implement the small host simulation library and its Makefile.
- [ ] Author and validate stages 5–6 with datasheet-style extracts, tracing work, driver code, and integration missions.
- [ ] Run platform tests, all reference solutions, and full Python tests.

### Task 8: Stages 7–8 — architecture and reliability

**Files:**
- Create: `curriculum/07-firmware-architecture/*`
- Create: `curriculum/08-reliability-tooling/*`
- Create: `tests/test_curriculum_architecture.py`

**Interfaces:**
- Adds missions for state machines, non-blocking event loops, ring buffers, callbacks, HAL boundaries, configuration, constraints, unit/integration testing, GDB, sanitizers, static analysis, concurrency hazards, fault investigation, and secure-C basics.

- [ ] Add coverage and reference-solution tests for every named topic and require at least one review, refactor, debugging, and multi-module integration activity.
- [ ] Verify tests fail for absent stages.
- [ ] Author guided missions with deterministic host checks and bounded timeouts.
- [ ] Run curriculum validation, reference checks, simulation tests, and the full unit suite.

### Task 9: Stage 9 — Library Forge

**Files:**
- Create: `curriculum/09-library-forge/*`
- Create: `examples/library-consumer/*`
- Create: `tests/test_library_forge.py`

**Interfaces:**
- Produces a portable example C library with public/private headers, CMake and Make consumers, semantic version metadata, generated install layout, API documentation, configuration points, and host tests.
- Adds missions that guide the learner through API design, encapsulation, compatibility, testing, documentation, packaging, and consumer integration.

- [ ] Add tests for clean build, public-header self-containment, install/consume flow, symbol encapsulation, version query, and invalid-input behavior.
- [ ] Verify focused tests fail.
- [ ] Implement the reference library and author all Stage 9 missions.
- [ ] Run both Make and CMake workflows, curriculum validation, and the full suite.

### Task 10: STM32 Nucleo-C031C6 track

**Files:**
- Create: `platforms/stm32c031/README.md`
- Create: `platforms/stm32c031/doctor.py`
- Create: `platforms/stm32c031/common/*`
- Create: `platforms/stm32c031/projects/*`
- Create: `curriculum/10-stm32-track/*`
- Create: `tests/test_stm32_track.py`

**Interfaces:**
- `doctor` reports presence and versions of the ARM compiler, CMake/Make, debugger/programmer tools, USB access hints, and board-specific requirements without flashing.
- Hardware missions expose explicit build and flash instructions; host stubs compile-check portable interfaces when ARM tools or hardware are unavailable.

- [ ] Add tests for doctor output with present/missing fake tools, no implicit flashing, project structure, interface compilation, and documented recovery paths.
- [ ] Verify focused tests fail.
- [ ] Author setup, known-good blink/UART, GPIO, timer/interrupt, ADC, and portable-module integration projects using official STM32 device support expected from the user's installed toolchain.
- [ ] Verify all host-side checks; conditionally compile ARM projects when the cross-toolchain is present, reporting a documented skip otherwise.

### Task 11: Stage 10 and sensor data-logger capstone

**Files:**
- Create: `curriculum/11-advanced/*`
- Create: `curriculum/12-capstone/*`
- Create: `capstone/reference/include/*`
- Create: `capstone/reference/src/*`
- Create: `capstone/reference/tests/*`
- Create: `capstone/reference/CMakeLists.txt`
- Create: `capstone/reference/Makefile`
- Create: `tests/test_capstone.py`

**Interfaces:**
- The portable capstone exposes typed sensor samples, validation, timestamp injection, ring-buffered records, serialization, storage and transport interfaces, deterministic host fakes, and a documented STM32 adapter boundary.
- Advanced missions cover startup, linker concepts, sections, boot flow, scheduling, real-time analysis, and RTOS concepts without making an RTOS dependency mandatory.

- [ ] Add capstone tests for valid/invalid samples, buffer wrap/full policy, timestamps, deterministic serialization, storage failures, transport retry policy, and a multi-session build checkpoint.
- [ ] Verify tests fail before the capstone exists.
- [ ] Implement the complete reference capstone, host demo, tests, build files, and learner campaign.
- [ ] Run Make, CMake/CTest, sanitizers when supported, curriculum validation, and full tests.

### Task 12: Complete-course polish and end-to-end verification

**Files:**
- Create: `README.md`
- Create: `docs/GETTING_STARTED.md`
- Create: `docs/CURRICULUM.md`
- Create: `docs/STM32_SETUP.md`
- Create: `scripts/test_all.sh`
- Create: `tests/test_end_to_end.py`

**Interfaces:**
- A new learner can run `./learn doctor`, `./learn map`, and `./learn start`; an author can run `./learn validate`; maintainers can run `./scripts/test_all.sh`.

- [ ] Add an end-to-end test using a temporary progress root: start, inspect lesson, test a failing attempt, copy the mission's solution into the attempt, pass, submit, unlock, replay, and resume.
- [ ] Verify the focused end-to-end test fails before final integration.
- [ ] Write user, curriculum, STM32, and maintenance documentation; ensure all command examples are executable.
- [ ] Run `./scripts/test_all.sh`; require zero failures, zero malformed missions, all reference solutions passing, host simulation and capstone green, and conditional STM32 checks clearly reported.
- [ ] Inspect a clean first-run experience and confirm no generated learner state is included in the shipped repository.

## Unresolved product decisions

None. The approved design and the explicit observable-command decisions above are sufficient to implement the complete repository. Physical STM32 execution cannot be automated without a connected board and installed vendor/cross tools; completion requires verified host-side project checks plus an explicit doctor report, while on-device observations remain learner-run hardware missions.
