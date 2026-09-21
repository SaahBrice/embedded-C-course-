#ifndef LEARN_SPI_TASK_H
#define LEARN_SPI_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool spi_build_read(uint8_t register_address, uint8_t *transaction, size_t capacity, size_t *out_length);

#endif
