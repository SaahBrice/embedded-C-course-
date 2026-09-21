#ifndef SIM_SPI_H
#define SIM_SPI_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define SIM_SPI_CAPACITY 64U

enum sim_spi_result { SIM_SPI_OK = 0, SIM_SPI_ARGUMENT, SIM_SPI_FULL, SIM_SPI_NOT_SELECTED };

void sim_spi_reset(void);
enum sim_spi_result sim_spi_set_response(const uint8_t *bytes, size_t count);
void sim_spi_select(bool selected);
enum sim_spi_result sim_spi_transfer(const uint8_t *tx, uint8_t *rx, size_t count);
size_t sim_spi_transaction_count(void);
size_t sim_spi_last_tx(uint8_t *destination, size_t capacity);

#endif
