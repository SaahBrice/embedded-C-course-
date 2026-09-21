#include "sim_i2c.h"

#include <string.h>

#define I2C_REGISTER_COUNT 256U
static uint8_t device_registers[I2C_REGISTER_COUNT];
static size_t device_register_count;
static uint8_t device_address;
static bool attached;
static enum sim_i2c_result next_failure;
static size_t transactions;

void sim_i2c_reset(void) {
    memset(device_registers, 0, sizeof device_registers);
    device_register_count = 0U;
    device_address = 0U;
    attached = false;
    next_failure = SIM_I2C_OK;
    transactions = 0U;
}

enum sim_i2c_result sim_i2c_attach(uint8_t address_7bit, const uint8_t *registers, size_t count) {
    if (address_7bit > UINT8_C(0x7f) || (registers == NULL && count != 0U)) return SIM_I2C_ARGUMENT;
    if (count > I2C_REGISTER_COUNT) return SIM_I2C_ARGUMENT;
    if (count != 0U) memcpy(device_registers, registers, count);
    device_register_count = count;
    device_address = address_7bit;
    attached = true;
    return SIM_I2C_OK;
}

void sim_i2c_fail_next(enum sim_i2c_result failure) {
    next_failure = (failure == SIM_I2C_NACK || failure == SIM_I2C_TIMEOUT) ? failure : SIM_I2C_OK;
}

enum sim_i2c_result sim_i2c_read_register(uint8_t address_7bit, uint8_t register_index, uint8_t *value) {
    if (value == NULL) return SIM_I2C_ARGUMENT;
    ++transactions;
    if (next_failure != SIM_I2C_OK) {
        const enum sim_i2c_result result = next_failure;
        next_failure = SIM_I2C_OK;
        return result;
    }
    if (!attached || address_7bit != device_address || register_index >= device_register_count) return SIM_I2C_ADDRESS;
    *value = device_registers[register_index];
    return SIM_I2C_OK;
}

size_t sim_i2c_transaction_count(void) { return transactions; }
