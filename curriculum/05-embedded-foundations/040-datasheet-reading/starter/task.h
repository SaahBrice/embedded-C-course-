#ifndef LEARN_DATASHEET_READING_TASK_H
#define LEARN_DATASHEET_READING_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool datasheet_field_encode(uint32_t value, unsigned shift, uint32_t mask, uint32_t *out_bits);

#endif
