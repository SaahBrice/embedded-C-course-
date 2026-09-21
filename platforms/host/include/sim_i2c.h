#ifndef SIM_I2C_H
#define SIM_I2C_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum sim_i2c_result { SIM_I2C_OK = 0, SIM_I2C_ARGUMENT, SIM_I2C_ADDRESS, SIM_I2C_NACK, SIM_I2C_TIMEOUT };

void sim_i2c_reset(void);
enum sim_i2c_result sim_i2c_attach(uint8_t address_7bit, const uint8_t *registers, size_t count);
void sim_i2c_fail_next(enum sim_i2c_result failure);
enum sim_i2c_result sim_i2c_read_register(uint8_t address_7bit, uint8_t register_index, uint8_t *value);
size_t sim_i2c_transaction_count(void);

#endif
