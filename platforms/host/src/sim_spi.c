#include "sim_spi.h"

#include <string.h>

static uint8_t response[SIM_SPI_CAPACITY];
static size_t response_count;
static uint8_t transmitted[SIM_SPI_CAPACITY];
static size_t transmitted_count;
static bool selected;
static size_t transactions;

void sim_spi_reset(void) {
    response_count = 0U;
    transmitted_count = 0U;
    selected = false;
    transactions = 0U;
}

enum sim_spi_result sim_spi_set_response(const uint8_t *bytes, size_t count) {
    if (bytes == NULL && count != 0U) return SIM_SPI_ARGUMENT;
    if (count > SIM_SPI_CAPACITY) return SIM_SPI_FULL;
    if (count != 0U) memcpy(response, bytes, count);
    response_count = count;
    return SIM_SPI_OK;
}

void sim_spi_select(bool value) { selected = value; }

enum sim_spi_result sim_spi_transfer(const uint8_t *tx, uint8_t *rx, size_t count) {
    if (!selected) return SIM_SPI_NOT_SELECTED;
    if ((tx == NULL || rx == NULL) && count != 0U) return SIM_SPI_ARGUMENT;
    if (count > SIM_SPI_CAPACITY || count > response_count) return SIM_SPI_FULL;
    if (count != 0U) {
        memcpy(transmitted, tx, count);
        memcpy(rx, response, count);
    }
    transmitted_count = count;
    ++transactions;
    return SIM_SPI_OK;
}

size_t sim_spi_transaction_count(void) { return transactions; }
size_t sim_spi_last_tx(uint8_t *destination, size_t capacity) {
    if (destination == NULL && capacity != 0U) return 0U;
    const size_t copied = transmitted_count < capacity ? transmitted_count : capacity;
    if (copied != 0U) memcpy(destination, transmitted, copied);
    return copied;
}
