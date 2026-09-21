# Test Collaborating Modules

## Your task

Define the interface in `task.c` so this rule holds: Deterministic fakes expose call count and transferred value, including read and storage failure branches between collaborating modules. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **fakes, contracts, failure injection** into behavior a caller can verify. In firmware, a defect in `bool`, `bool`, `logger_cycle` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `bool`, `bool`, `logger_cycle`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
struct logger_ports { void *context; bool (*read)(void *, int32_t *); bool (*store)(void *, int32_t); };
bool logger_cycle(const struct logger_ports *ports);
```

Do not change these declarations.

- `ports` from `const struct logger_ports *ports`: read-only input accessed through a pointer; null handling follows the contract.
- `logger_cycle` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct fake_logger f={true,true,42,0,0U,0U}; struct logger_ports p={&f,fake_logger_read,fake_logger_store}; assert(logger_cycle(&p)&&f.stored==42&&f.reads==1U&&f.writes==1U); f.read_ok=false; assert(!logger_cycle(&p)&&f.writes==1U); f.read_ok=true; f.store_ok=false; assert(!logger_cycle(&p));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
