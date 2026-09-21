#include "app.h"
#include "board_host.h"

#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int reject_uart(void *context, const char *text, size_t length) {
    (void)context;
    (void)text;
    (void)length;
    return 0;
}

int main(void) {
    struct board_host board;
    struct app app;
    board_host_reset(&board);
    const struct app_port port = {&board, board_host_set_led, board_host_write_uart};
    assert(app_init(&app, &port, UINT32_MAX - 100U));
    assert(board.led_writes == 1U && board.led_on == 0);
    assert(strcmp(board.uart, "NUCLEO-C031C6 app ready\r\n") == 0);
    app_step(&app, 398U);
    assert(board.led_writes == 1U);
    app_step(&app, 399U);
    assert(board.led_writes == 2U && board.led_on == 1);
    app_step(&app, 899U);
    assert(board.led_writes == 3U && board.led_on == 0);

    const struct app_port failing_port = {&board, board_host_set_led, reject_uart};
    assert(!app_init(&app, &failing_port, 0U));
    puts("stm32 app host contract: passed");
    return 0;
}
