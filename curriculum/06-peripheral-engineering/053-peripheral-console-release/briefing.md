# Release: Peripheral Console

## Your task

Define the interface in `task.c` so this rule holds: The peripheral-console release parses complete UART text into typed commands, classifies actuator work, and converts a logical LED request to the configured electrical level. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **GPIO, timer, UART, ADC** into behavior a caller can verify. In firmware, a defect in `console_parse`, `console_is_led_command`, `console_led_level` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `console_parse`, `console_is_led_command`, `console_led_level`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
enum console_command { CONSOLE_INVALID, CONSOLE_LED_ON, CONSOLE_LED_OFF, CONSOLE_READ_ADC };
enum console_command console_parse(const char *line);
bool console_is_led_command(enum console_command command);
bool console_led_level(enum console_command command, bool active_low, bool *out_level);
```

Do not change these declarations.

- `line` from `const char *line`: read-only input accessed through a pointer; null handling follows the contract.
- `console_parse` return type `enum console_command`: returns one of the named status or state values declared above.
- `command` from `enum console_command command`: an input value; its meaningful range is demonstrated below.
- `console_is_led_command` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `command` from `enum console_command command`: an input value; its meaningful range is demonstrated below.
- `active_low` from `bool active_low`: a true/false input flag.
- `out_level` from `bool *out_level`: caller-owned destination written only when the operation succeeds.
- `console_led_level` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
bool level=false;assert(console_parse("LED ON")==CONSOLE_LED_ON);assert(console_parse("READ ADC")==CONSOLE_READ_ADC);assert(console_is_led_command(CONSOLE_LED_OFF));assert(!console_is_led_command(CONSOLE_READ_ADC));assert(console_led_level(CONSOLE_LED_ON,false,&level)&&level);assert(console_led_level(CONSOLE_LED_ON,true,&level)&&!level);assert(!console_led_level(CONSOLE_READ_ADC,false,&level));assert(console_parse("LED")==CONSOLE_INVALID);
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
