#ifndef LEARN_I2C_TASK_H
#define LEARN_I2C_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool i2c_address_byte(uint8_t address_7bit, bool read, uint8_t *out_byte);

#endif
