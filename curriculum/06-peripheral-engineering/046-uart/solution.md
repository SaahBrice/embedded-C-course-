# Full solution: Build a UART Boundary

This worked implementation demonstrates baud, TX/RX, framing, buffers. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Build a UART Boundary */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

enum uart_feed_result uart_line_feed(struct uart_line *line, char byte) {
    if (line == NULL) return UART_OVERFLOW;
    if (byte == '\n') { line->bytes[line->length] = '\0'; return UART_READY; }
    if (line->length + 1U >= UART_LINE_CAPACITY) return UART_OVERFLOW;
    line->bytes[line->length++] = byte;
    line->bytes[line->length] = '\0';
    return UART_MORE;
}
```
