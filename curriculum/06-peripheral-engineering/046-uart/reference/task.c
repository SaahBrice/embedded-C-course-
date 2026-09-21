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
