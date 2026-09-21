# Getting Started

## Requirements

The host campaign runs on Linux with Python 3.11+ and GCC or Clang. GNU Make and CMake are used by later library projects. Run `./learn doctor` to inspect the tools already available. ARM and STM32 tools are not required for early or simulated sublevels; the hardware checkpoint explains them when you reach it.

## Levels and sublevels

The learning hierarchy is:

```text
Course
  Level
    ordered coding sublevels
    final battle (the last sublevel)
```

A level groups related concepts around one main objective. Every sublevel is a different coding problem, not another test mode for the same problem. You complete them in order. Passing an ordinary sublevel unlocks the next sublevel; passing the final battle clears the level and unlocks the next level.

Run `./learn map` to see `CLEARED`, `DONE`, `READY`, and `LOCKED` states. Run `./learn level` for the current level overview or `./learn sublevels` for its ordered checklist.

## Your first session

Run:

```bash
./learn map
./learn start
```

On first entry, `start` displays the level objective and then the first sublevel briefing. It creates a numbered attempt below `.learn/attempts/` and prints the exact path. Open that directory in your editor. The copied `BRIEFING.md` stays beside your source, so you never have to rely on terminal scrollback.

Do not edit files below `curriculum/`; they are the course source. Edit only the attempt workspace. `./learn status` always shows the active level, sublevel, workspace, and briefing path. `./learn continue` starts or resumes the next required sublevel.

Every briefing contains only five useful sections:

- the precise coding job;
- why the concept matters in firmware and what is wrong with the starter;
- the declaration and meaning of its parameters;
- normal, boundary, and failure examples;
- the expected behavior when an input or operation must be rejected.

The first sublevel gives you one complete, tiny program: edit the existing `main` in `main.c`, print the required line, and return success. The second sublevel introduces a reusable function: define `firmware_status` in `task.c`. In that function-only exercise, do not create `main` and do not change `task.h`; the visible and immutable drivers provide `main`.

## The coding loop

Use this loop as often as needed:

```bash
./learn run
./learn test
./learn hint
./learn solution
./learn submit
```

`./learn run` is the transparent execution bridge for function-only work. It builds your real source with a trusted temporary `main`, prints compiler warnings or errors, and shows visible expected/actual results. Some complete-program or project sublevels use their natural runner instead.

`./learn test` runs the complete immutable contract. Fix the first useful diagnostic, rerun, and compare behavior at zero, ordinary, maximum, and invalid inputs. You never need to write a reflection.

`./learn hint` reveals the next hint. `./learn solution` explains a complete implementation without altering progress. Different C code is correct when it preserves the same interface, behavior, boundaries, and defined C semantics.

When checks pass, `./learn submit` records completion atomically. Continue until the final battle; its successful submission prints `LEVEL CLEARED` and unlocks the next level.

## Sessions and replay

A normal sublevel targets 45–60 minutes, while final battles may take several sessions. Workspaces persist. Running `./learn start` or `./learn continue` later resumes the current work.

After completion, `./learn replay <sublevel-id>` creates a fresh numbered workspace. `./learn replay-final <level-id>` replays the final battle of a cleared level. Previous attempts remain available for comparison.

Hardware checkpoints combine an automated ARM build with a structured record of what you personally observed after an explicit flash. The record is self-attestation; host software never pretends it saw a physical LED or UART signal.

## Example session

This is the complete shape of an ordinary session; the exact diagnostics depend on the code you write:

```text
$ ./learn map
[READY] Level 1: Orientation and Toolchain
    [READY] Build Your First C Program (first-build)

$ ./learn start
Level 1: Orientation and Toolchain
Sublevel: Build Your First C Program
Workspace: .../.learn/attempts/first-build--001
Open .../BRIEFING.md, edit main.c, then run './learn run' or './learn test'.

$ ./learn run
firmware ready
Process exit status: 0

$ ./learn test
[PASS] Strict build and immutable behavior tests

$ ./learn submit
Sublevel complete: Build Your First C Program
Next sublevel unlocked: Implement Your First Firmware Function. Run './learn continue'.

$ ./learn continue
Sublevel: Implement Your First Firmware Function

$ ./learn run
Call and inputs: firmware_status(0U)
  Actual return: -1
Case 1
  Expected condition: firmware_status(0U) == -1
  Observed condition: true
  Result: PASS
```

Repeat the run–test–submit loop for each ordered sublevel. The last submission in the level ends with `LEVEL CLEARED: Orientation and Toolchain`; then `./learn continue` enters Level 2.
