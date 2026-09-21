# Version an Embedded Library

## Your task

Define the interface in `task.c` so this rule holds: A breaking public change is major, a backward-compatible addition is minor, and an internal fix is patch. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **major, minor, patch, compatibility** into behavior a caller can verify. In firmware, a defect in `classify_version_change` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `classify_version_change`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
enum version_change { VERSION_PATCH, VERSION_MINOR, VERSION_MAJOR };
enum version_change classify_version_change(bool breaks_api, bool adds_api);
```

Do not change these declarations.

- `breaks_api` from `bool breaks_api`: a true/false input flag.
- `adds_api` from `bool adds_api`: a true/false input flag.
- `classify_version_change` return type `enum version_change`: returns one of the named status or state values declared above.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(classify_version_change(false,false)==VERSION_PATCH); assert(classify_version_change(false,true)==VERSION_MINOR); assert(classify_version_change(true,false)==VERSION_MAJOR); assert(classify_version_change(true,true)==VERSION_MAJOR);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
