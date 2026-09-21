#include "task.h"
#include "sim_uart.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static enum uart_feed_result visible_return_uart_line_feed(const char *call, enum uart_feed_result value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define uart_line_feed(...) visible_return_uart_line_feed("uart_line_feed(" #__VA_ARGS__ ")", (uart_line_feed)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 8

static unsigned visible_case_number;
static unsigned visible_failures;

static void visible_check(int passed, const char *expression) {
    printf("Case %u\n  Expected condition: %s\n  Observed condition: %s\n  Result: %s\n",
           visible_case_number, expression, passed ? "true" : "false",
           passed ? "PASS" : "FAIL");
    if (!passed) ++visible_failures;
}

#define assert(expression) do {     ++visible_case_number;     visible_check(!!(expression), #expression); } while (0)

int main(void) {
    struct uart_line line = {{0},0U}; assert(uart_line_feed(&line,'O')==UART_MORE); assert(uart_line_feed(&line,'K')==UART_MORE); assert(uart_line_feed(&line,'\n')==UART_READY); assert(strcmp(line.bytes,"OK")==0); struct uart_line full={{0},7U}; assert(uart_line_feed(&full,'x')==UART_OVERFLOW);
    const uint8_t received[]={'O','K','\n'}; struct uart_line simulated={{0},0U}; uint8_t incoming=0U; sim_uart_reset(); assert(sim_uart_inject_rx(received,sizeof received)==SIM_UART_OK); while(sim_uart_read(&incoming)==SIM_UART_OK)(void)uart_line_feed(&simulated,(char)incoming); assert(strcmp(simulated.bytes,"OK")==0); assert(sim_uart_write((const uint8_t *)simulated.bytes,simulated.length)==SIM_UART_OK&&sim_uart_tx_pending()==2U);
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
