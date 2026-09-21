#ifndef LEARN_REGISTER_DRIVER_RELEASE_TASK_H
#define LEARN_REGISTER_DRIVER_RELEASE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool gpio_pin_valid(unsigned pin);
bool gpio_mode_set(uint32_t original, unsigned pin, uint32_t mode, uint32_t *out_value);
bool gpio_mode_matches(uint32_t register_value, unsigned pin, uint32_t expected_mode);

#endif
