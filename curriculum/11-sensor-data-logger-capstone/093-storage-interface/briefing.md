# Capstone: Persist Records

## Your task

Define the interface in `task.c` so this rule holds: The orchestration retains ownership until every byte is acknowledged, supports valid partial writes, and stops on zero progress. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **storage port, partial write, retry ownership** into behavior a caller can verify. In firmware, a defect in `size_t`, `storage_write_all` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `size_t`, `storage_write_all`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
typedef size_t (*storage_write_fn)(void *context, const uint8_t *bytes, size_t length);
bool storage_write_all(storage_write_fn write, void *context, const uint8_t *bytes, size_t length);
```

Do not change these declarations.

- `context` from `*storage_write_fn)(void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `size_t` return type `typedef`: returns the result or status defined by the required behavior.
- `write` from `storage_write_fn write`: an input value; its meaningful range is demonstrated below.
- `context` from `void *context`: opaque state owned by the caller; its lifetime must cover the call.
- `bytes` from `const uint8_t *bytes`: read-only input accessed through a pointer; null handling follows the contract.
- `length` from `size_t length`: number of elements or bytes available; zero is a boundary case.
- `storage_write_all` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
const uint8_t data[]={1U,2U,3U,4U,5U}; struct fake_storage s={{0U},0U,2U,false}; assert(storage_write_all(fake_storage_write,&s,data,sizeof data)&&s.length==5U&&memcmp(s.bytes,data,5U)==0); s.length=0U;s.fail=true;assert(!storage_write_all(fake_storage_write,&s,data,sizeof data));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
