/* Mission: Acquire Analog Samples */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool adc_code_to_mv(uint16_t code, uint8_t resolution_bits, uint16_t reference_mv, uint16_t *out_mv) {
    if (out_mv == NULL || resolution_bits == 0U || resolution_bits > 16U || reference_mv == 0U) return false;
    const uint32_t maximum = (UINT32_C(1) << resolution_bits) - 1U;
    if (code > maximum) return false;
    *out_mv = (uint16_t)(((uint32_t)code * reference_mv + maximum / 2U) / maximum);
    return true;
}
