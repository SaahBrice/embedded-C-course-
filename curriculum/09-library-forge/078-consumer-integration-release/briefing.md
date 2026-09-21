# Release: Record Queue Library

## Your task

This final battle starts on the other side of a library boundary. The trusted harness creates an installed prefix containing only `include/rq.h` and `lib/librq.a`. Your `consumer.c` must use that public installation as an ordinary external dependency; it cannot include private source or rely on a source-tree path.

Edit `consumer.c` in the attempt directory printed by `./learn status`. Do not edit anything below `curriculum/` or the trusted checker files. `./learn run` will build the installed-only fixture, compile your consumer, and run it without submitting; it prints the real build output and first diagnostic. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

The final proof of a C library is a separate consumer. Building against installed-only paths catches leaked private headers, missing archive symbols, and accidental dependence on the library source tree—problems that unit tests inside the library can miss.

The starter already includes the installed public header, but `main` returns failure without checking the API. Use `rq_version()` and `rq_add()` through that header. Return zero only when the version is exactly `1.0.0` and `rq_add(19, 23)` returns `42`.

## Read the function signature

This is a multi-file or hardware sublevel; the editable artifacts are named below.

## Concrete examples

- The strict consumer compile must find `<rq.h>` only through the temporary installed include directory.
- The link must resolve calls only from the installed `librq.a`.
- Version `1.0.0` and the result `42` mean success and `main` returns `0`; any mismatch returns a nonzero status.

## Expected failure behavior

Return a nonzero value if the version or arithmetic result differs. A missing public declaration or symbol must fail naturally at compile or link time.
