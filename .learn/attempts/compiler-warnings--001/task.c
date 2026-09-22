

#include "task.h"

bool adc_to_millivolts(uint16_t code, uint16_t reference_mv, uint16_t *out_mv) {
    if (out_mv == NULL || code > UINT16_C(4095) || reference_mv == 0U) return false;
    *out_mv = (uint16_t)((uint32_t)code * (uint32_t)reference_mv / UINT32_C(4095)); /* diagnose the conversion and range defects */
    return true;
}
