#ifndef LEARN_COMPILER_WARNINGS_TASK_H
#define LEARN_COMPILER_WARNINGS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool adc_to_millivolts(uint16_t code, uint16_t reference_mv, uint16_t *out_mv);

#endif
