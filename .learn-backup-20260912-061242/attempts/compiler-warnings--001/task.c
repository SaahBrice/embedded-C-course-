#include "task.h"
bool adc_to_millivolts(uint16_t code, uint16_t reference_mv, uint16_t *out_mv) {
    if (out_mv == NULL) return false;
    *out_mv = code * reference_mv / 4095; /* diagnose the conversion and range defects */
    return true;
}
