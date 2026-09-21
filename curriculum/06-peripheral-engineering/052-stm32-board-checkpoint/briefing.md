# Bring Up the Nucleo-C031C6

## Your task

This hardware sublevel uses the repository's STM32 project rather than asking for a new `task.c`. Build the ARM ELF first. Flashing is always a separate explicit command. Record only LED and UART behavior you personally observed on the NUCLEO-C031C6.

Edit `build-report.txt` and `hardware-evidence.json` in the attempt directory printed by `./learn status`. Do not edit anything below `curriculum/` or the trusted checker files. `./learn run` will validate the recorded ARM build report and hardware evidence; it never flashes the board without submitting; it prints the real build output and first diagnostic. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

Host simulations prove portable logic, but only a target build and explicit flash exercise the real compiler, linker, debug probe, pins, and board wiring. Separating machine-checked build evidence from your physical observations keeps the result honest and reproducible.

The starter evidence files are examples, not claims about your desk. Replace their fields with the build command, ELF information, flash tool, and observations you actually obtained. Never report a flash or LED result that did not happen.

## Read the function signature

This is a multi-file or hardware sublevel; the editable artifacts are named below.

## Concrete examples

- The build report names the ARM command and identifies the output as an ARM ELF.
- The hardware record names the NUCLEO-C031C6, the confirmed flash tool, and your actual PA5 LED and USART2 observations.
- If hardware is unavailable, leave this sublevel incomplete rather than inventing evidence.

## Expected failure behavior

A missing tool or disconnected board is reported as unavailable evidence, never converted into a successful observation. Ordinary `run`, `test`, and repository validation never flash hardware.
