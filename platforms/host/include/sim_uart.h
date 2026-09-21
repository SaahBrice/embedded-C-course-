#ifndef SIM_UART_H
#define SIM_UART_H

#include <stddef.h>
#include <stdint.h>

#define SIM_UART_CAPACITY 256U

enum sim_uart_result { SIM_UART_OK = 0, SIM_UART_ARGUMENT, SIM_UART_FULL, SIM_UART_EMPTY };

void sim_uart_reset(void);
enum sim_uart_result sim_uart_inject_rx(const uint8_t *data, size_t count);
enum sim_uart_result sim_uart_read(uint8_t *value);
enum sim_uart_result sim_uart_write(const uint8_t *data, size_t count);
size_t sim_uart_drain_tx(uint8_t *destination, size_t capacity);
size_t sim_uart_rx_pending(void);
size_t sim_uart_tx_pending(void);

#endif
