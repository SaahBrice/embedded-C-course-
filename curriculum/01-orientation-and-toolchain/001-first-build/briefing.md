# Build Your First C Program

## Your task

This is a complete C program, so you **do** edit the supplied `main` function in `main.c`. `main` is where a hosted C program begins. `puts` writes text and automatically adds a newline. Returning zero from `main` tells the terminal that the program succeeded.

Edit `main.c` in the attempt directory printed by `./learn status`. Do not create a second `main` or edit anything below `curriculum/`. `./learn run` compiles and executes `main.c`, showing its output and exit status. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

Command-line build tools and automated firmware pipelines observe both output bytes and process status. This exercise makes those two interfaces visible: the newline is part of stdout, and zero from `main` is the operating system's success signal.

The starter prints `firmware pending` and returns `1`, so both observable results violate the assignment. Change the string to exactly `firmware ready` and return `0`.

## Read the function signature

`main.c` already contains `int main(void)`. Edit that function; do not create a second entry point.

## Concrete examples

- Standard output must contain exactly `firmware ready` followed by one newline.
- The process exit status must be `0`.
- Extra spaces, extra lines, different capitalization, or returning `1` are failures because another tool may consume this exact interface.

## Expected failure behavior

If either observable result is wrong, the checker reports the actual output or exit status and rejects the submission. A compiler warning also fails the strict build.
