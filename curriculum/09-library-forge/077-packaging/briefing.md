# Install and Package a C Library

## Your task

This is a multi-file build exercise. You are producing a static C library that can be installed into a temporary prefix and used by a consumer that has no path back into the source tree. Both Make and CMake must describe the same public header and archive.

Edit `rq.c`, `rq.h`, `Makefile`, and `CMakeLists.txt` in the attempt directory printed by `./learn status`. Do not edit anything below `curriculum/` or the trusted checker files. `./learn run` will execute the trusted Make/CMake build and relocation check without submitting; it prints the real build output and first diagnostic. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

A reusable library is more than source that builds inside its own directory. Firmware teams need a public header, archive, version, and install layout that another project can consume without private paths. Make and CMake must publish the same boundary.

Inspect `rq.c`, `rq.h`, `Makefile`, and `CMakeLists.txt`. The starter reports the wrong public version or leaves the package/consumer contract incomplete. Repair the supplied files; do not create `task.c` or change the trusted project harness.

## Read the function signature

This is a multi-file or hardware sublevel; the editable artifacts are named below.

## Concrete examples

- `make ... install PREFIX=<temporary-directory>` must place `rq.h` under `include` and `librq.a` under `lib`.
- A separate program compiled with only that installed prefix must include `<rq.h>`, link the archive, and observe version `1.0.0`.
- A clean CMake configure, build, and install must provide the same result.

## Expected failure behavior

A compile, archive, install, link, version, or relocated execution error returns nonzero and prints the real failing command's output. No source-tree include fallback is accepted.
