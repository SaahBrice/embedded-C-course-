#ifndef BOARD_HOST_H
#define BOARD_HOST_H

#include <stddef.h>

struct board_host {
    int led_on;
    unsigned led_writes;
    char uart[128];
    size_t uart_length;
};

void board_host_reset(struct board_host *host);
void board_host_set_led(void *context, int on);
int board_host_write_uart(void *context, const char *text, size_t length);

#endif
