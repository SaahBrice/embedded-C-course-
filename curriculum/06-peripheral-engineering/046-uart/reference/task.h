#ifndef LEARN_UART_TASK_H
#define LEARN_UART_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define UART_LINE_CAPACITY 8U
struct uart_line { char bytes[UART_LINE_CAPACITY]; size_t length; };
enum uart_feed_result { UART_MORE, UART_READY, UART_OVERFLOW };
enum uart_feed_result uart_line_feed(struct uart_line *line, char byte);

#endif
