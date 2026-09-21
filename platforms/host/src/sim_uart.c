#include "sim_uart.h"

#include <string.h>

struct byte_queue {
    uint8_t data[SIM_UART_CAPACITY];
    size_t head;
    size_t tail;
    size_t count;
};

static struct byte_queue rx;
static struct byte_queue tx;

static enum sim_uart_result push(struct byte_queue *queue, const uint8_t *data, size_t count) {
    if (data == NULL && count != 0U) return SIM_UART_ARGUMENT;
    if (count > SIM_UART_CAPACITY - queue->count) return SIM_UART_FULL;
    for (size_t index = 0U; index < count; ++index) {
        queue->data[queue->head] = data[index];
        queue->head = (queue->head + 1U) % SIM_UART_CAPACITY;
        queue->count++;
    }
    return SIM_UART_OK;
}

static enum sim_uart_result pop(struct byte_queue *queue, uint8_t *value) {
    if (value == NULL) return SIM_UART_ARGUMENT;
    if (queue->count == 0U) return SIM_UART_EMPTY;
    *value = queue->data[queue->tail];
    queue->tail = (queue->tail + 1U) % SIM_UART_CAPACITY;
    queue->count--;
    return SIM_UART_OK;
}

void sim_uart_reset(void) {
    memset(&rx, 0, sizeof rx);
    memset(&tx, 0, sizeof tx);
}

enum sim_uart_result sim_uart_inject_rx(const uint8_t *data, size_t count) { return push(&rx, data, count); }
enum sim_uart_result sim_uart_read(uint8_t *value) { return pop(&rx, value); }
enum sim_uart_result sim_uart_write(const uint8_t *data, size_t count) { return push(&tx, data, count); }

size_t sim_uart_drain_tx(uint8_t *destination, size_t capacity) {
    if (destination == NULL && capacity != 0U) return 0U;
    size_t copied = 0U;
    while (copied < capacity && pop(&tx, &destination[copied]) == SIM_UART_OK) copied++;
    return copied;
}

size_t sim_uart_rx_pending(void) { return rx.count; }
size_t sim_uart_tx_pending(void) { return tx.count; }
