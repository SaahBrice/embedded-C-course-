# Build a UART Boundary

## Your task

Define the interface in `task.c` so this rule holds: `uart_line_feed` accepts one byte per call, always preserves termination, reports a complete line at newline, and rejects overflow. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **baud, TX/RX, framing, buffers** into behavior a caller can verify. In firmware, a defect in `uart_line_feed` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `uart_line_feed`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
#define UART_LINE_CAPACITY 8U
struct uart_line { char bytes[UART_LINE_CAPACITY]; size_t length; };
enum uart_feed_result { UART_MORE, UART_READY, UART_OVERFLOW };
enum uart_feed_result uart_line_feed(struct uart_line *line, char byte);
```

Do not change these declarations.

- `line` from `struct uart_line *line`: pointer to caller-owned state that the function may update.
- `byte` from `char byte`: an input value; its meaningful range is demonstrated below.
- `uart_line_feed` return type `enum uart_feed_result`: returns one of the named status or state values declared above.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
struct uart_line line = {{0},0U}; assert(uart_line_feed(&line,'O')==UART_MORE); assert(uart_line_feed(&line,'K')==UART_MORE); assert(uart_line_feed(&line,'\n')==UART_READY); assert(strcmp(line.bytes,"OK")==0); struct uart_line full={{0},7U}; assert(uart_line_feed(&full,'x')==UART_OVERFLOW);
```

## Expected failure behavior

Return the named failure or safe-state enumerator for rejected work; never invent an out-of-range enum result or partially publish output.
