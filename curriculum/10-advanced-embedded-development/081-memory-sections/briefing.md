# Place Data Deliberately

## Your task

Define the interface in `task.c` so this rule holds: Mutability, initializer value, and reset retention select the intended object section. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **text, rodata, data, bss, noinit** into behavior a caller can verify. In firmware, a defect in `choose_object_section` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `choose_object_section`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
enum object_section { SECTION_RODATA, SECTION_DATA, SECTION_BSS, SECTION_NOINIT };
enum object_section choose_object_section(bool writable, bool has_nonzero_initializer, bool retain_across_reset);
```

Do not change these declarations.

- `writable` from `bool writable`: a true/false input flag.
- `has_nonzero_initializer` from `bool has_nonzero_initializer`: a true/false input flag.
- `retain_across_reset` from `bool retain_across_reset`: a true/false input flag.
- `choose_object_section` return type `enum object_section`: returns one of the named status or state values declared above.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(choose_object_section(false,true,false)==SECTION_RODATA); assert(choose_object_section(true,true,false)==SECTION_DATA); assert(choose_object_section(true,false,false)==SECTION_BSS); assert(choose_object_section(true,false,true)==SECTION_NOINIT);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
