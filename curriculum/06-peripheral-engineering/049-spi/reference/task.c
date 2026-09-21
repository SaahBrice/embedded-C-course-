/* Mission: Transact over SPI */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool spi_build_read(uint8_t register_address, uint8_t *transaction, size_t capacity, size_t *out_length) {
    if (transaction == NULL || out_length == NULL || capacity < 2U || register_address > 0x7fU) return false;
    transaction[0] = (uint8_t)(register_address | 0x80U);
    transaction[1] = 0xffU;
    *out_length = 2U;
    return true;
}
