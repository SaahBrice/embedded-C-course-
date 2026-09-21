/* Mission: Treat Warnings as Defects */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool adc_to_millivolts(uint16_t code, uint16_t reference_mv, uint16_t *out_mv) {
    if (out_mv == NULL || code > UINT16_C(4095) || reference_mv == 0U) return false;
    const uint32_t scaled = (uint32_t)code * reference_mv + UINT32_C(2047);
    *out_mv = (uint16_t)(scaled / UINT32_C(4095));
    return true;
}
