# Level 9: Library Forge

## Main objective

Turn embedded C into a documented, versioned, configurable, tested, installable library with private internals.

## What you should know before starting

Complete Level 8; this level builds directly on its C contracts and debugging habits.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Release: Record Queue Library**.

## What you will build and learn

- Design a documented public API while keeping representation private
- Version, configure, test, build, install, and relocate a static C library
- Prove a consumer can use the record-queue library without source-tree access

## Ordered sublevels

1. **Design a Stable Library API** (`api-design`) — Implement `counter_add_bounded`: The public operation exposes a narrow status-returning contract and never publishes a value beyond its configured limit.
2. **Hide Library Internals** (`encapsulation`) — Implement `record_queue_required_bytes`, `record_queue_init`, `record_queue_push`, `record_queue_pop`: Consumers can name only the opaque queue type; storage sizing and every invariant remain owned by the implementation.
3. **Version an Embedded Library** (`semantic-versioning`) — Implement `classify_version_change`: A breaking public change is major, a backward-compatible addition is minor, and an internal fix is patch.
4. **Configure Without Forking** (`library-configuration`) — Implement `queue_config_valid`: Queue configuration accepts only supported power-of-two capacities while treating policy as an explicit option.
5. **Document Contracts and Examples** (`library-documentation`) — Implement `documented_copy`: The executable API matches a documentable ownership, nullability, capacity, and zero-length contract.
6. **Build a Library Test Matrix** (`library-testing`) — Implement `ring_state_valid`: Tests can state and exercise empty, full, wrapped, and invalid ring-buffer invariants independently of implementation.
7. **Install and Package a C Library** (`packaging`) — Repair, build, install, and relocate a static record-queue library with Make and CMake.
8. **Release: Record Queue Library** (`consumer-integration-release`) — FINAL BATTLE — Prove a clean consumer can compile and link only against the installed record-queue package.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **public API and encapsulation** is practised in: Design a Stable Library API, Hide Library Internals, Version an Embedded Library, Configure Without Forking, Document Contracts and Examples, Release: Record Queue Library
- **verification and release discipline** is practised in: Version an Embedded Library, Document Contracts and Examples, Build a Library Test Matrix, Install and Package a C Library, Release: Record Queue Library
- **build, install, and compatibility** is practised in: Configure Without Forking, Document Contracts and Examples, Build a Library Test Matrix, Install and Package a C Library, Release: Record Queue Library

## Final battle

**Release: Record Queue Library** is the last required sublevel. It integrates **Document Contracts and Examples**, **Build a Library Test Matrix**, **Install and Package a C Library**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
