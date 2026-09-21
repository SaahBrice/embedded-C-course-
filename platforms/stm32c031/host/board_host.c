#include "board_host.h"

#include <string.h>

void board_host_reset(struct board_host *host) {
    if (host != NULL) memset(host, 0, sizeof *host);
}

void board_host_set_led(void *context, int on) {
    struct board_host *host = context;
    if (host == NULL) return;
    host->led_on = on != 0;
    host->led_writes++;
}

int board_host_write_uart(void *context, const char *text, size_t length) {
    struct board_host *host = context;
    if (host == NULL || text == NULL) return 0;
    const size_t available = sizeof host->uart - host->uart_length - 1U;
    if (length > available) length = available;
    memcpy(host->uart + host->uart_length, text, length);
    host->uart_length += length;
    host->uart[host->uart_length] = '\0';
    return 1;
}
