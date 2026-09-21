# Install and Package a C Library

## What you are doing

Build, install into a temporary prefix, and consume the library without source-tree-relative includes. In this version of the exercise you learn by changing and running real C artifacts; there is no reflection or essay to submit.

## Why firmware engineers care

The key ideas are **Make, CMake, install layout, export**. Firmware must keep behaving at boundaries and after unusual inputs, not merely in one demonstration. This exercise turns those ideas into behavior the compiler and tests can observe.

## Files you will edit

Edit `rq.c`, `rq.h`, `Makefile`, and `CMakeLists.txt`. Do not edit files below `curriculum/` or the hidden acceptance harness. Your personal copy is inside the attempt workspace printed by `./learn status`.

## Required behavior

The concrete `library/record_queue` project installs public headers under `include`, the archive under `lib`, exports CMake metadata, and proves relocation by building `examples/library-consumer` against a temporary prefix with no source-tree include path.

## A practical way to begin

1. Read the complete starter and public interface before changing it.
2. Find the placeholder or deliberate defect and predict the first failing case.
3. Make the smallest correct change while keeping strict compiler warnings enabled.
4. Run `./learn test` and address the first useful diagnostic.
5. Check the zero/empty case, an ordinary case, and the first invalid or maximum case.

## Common mistake

Do not weaken the function signature, compiler flags, error result, or bounds just to make one example work. A passing implementation must preserve the contract for callers that you cannot see.

## Success looks like

Build, install, and consume the library successfully with both Make and CMake. Run `./learn test`; every required check must report `PASS`. Use `./learn solution` whenever you need the worked implementation—solutions carry no penalty.
