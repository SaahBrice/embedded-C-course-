#ifndef LEARN_MODULAR_LIBRARY_RELEASE_TASK_H
#define LEARN_MODULAR_LIBRARY_RELEASE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

uint8_t crc8_update(uint8_t crc, uint8_t byte);
uint8_t crc8(const uint8_t *bytes, size_t length);
bool crc8_verify(const uint8_t *bytes, size_t length, uint8_t expected);

#endif
