#ifndef LEARN_INPUT_VALIDATION_TASK_H
#define LEARN_INPUT_VALIDATION_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool parse_u16(const char *text, uint16_t *out_value);

#endif
