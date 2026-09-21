#ifndef LEARN_ADC_TASK_H
#define LEARN_ADC_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool adc_code_to_mv(uint16_t code, uint8_t resolution_bits, uint16_t reference_mv, uint16_t *out_mv);

#endif
