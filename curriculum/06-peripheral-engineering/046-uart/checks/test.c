#include "task.h"
#include "sim_uart.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    struct uart_line line = {{0},0U}; assert(uart_line_feed(&line,'O')==UART_MORE); assert(uart_line_feed(&line,'K')==UART_MORE); assert(uart_line_feed(&line,'\n')==UART_READY); assert(strcmp(line.bytes,"OK")==0); struct uart_line full={{0},7U}; assert(uart_line_feed(&full,'x')==UART_OVERFLOW);
    const uint8_t received[]={'O','K','\n'}; struct uart_line simulated={{0},0U}; uint8_t incoming=0U; sim_uart_reset(); assert(sim_uart_inject_rx(received,sizeof received)==SIM_UART_OK); while(sim_uart_read(&incoming)==SIM_UART_OK)(void)uart_line_feed(&simulated,(char)incoming); assert(strcmp(simulated.bytes,"OK")==0); assert(sim_uart_write((const uint8_t *)simulated.bytes,simulated.length)==SIM_UART_OK&&sim_uart_tx_pending()==2U);
    return 0;
}
