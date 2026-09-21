#ifndef LEARN_DATA_LOGGER_RELEASE_TASK_H
#define LEARN_DATA_LOGGER_RELEASE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool logger_record_shape_valid(const uint8_t *bytes, size_t length);
uint32_t logger_release_checksum(const uint8_t *bytes, size_t length);
bool logger_release_validate(const uint8_t *bytes, size_t length, uint32_t expected_checksum);

#endif
