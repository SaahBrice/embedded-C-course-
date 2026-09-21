/* Mission: Write Portable C */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool read_u32_le(const uint8_t *bytes, size_t length, uint32_t *out_value) {
    if (bytes == NULL || out_value == NULL || length < 4U) return false;
    *out_value = (uint32_t)bytes[0] | ((uint32_t)bytes[1] << 8U) | ((uint32_t)bytes[2] << 16U) | ((uint32_t)bytes[3] << 24U); return true;
}
