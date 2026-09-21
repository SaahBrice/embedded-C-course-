/* Mission: Manipulate Register Bits */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool register_field_write(uint32_t original, uint32_t mask, unsigned shift, uint32_t field_value, uint32_t *out_value) {
    if (out_value == NULL || mask == 0U || shift >= 32U || (mask >> shift) == 0U || (field_value & ~(mask >> shift)) != 0U) return false;
    *out_value = (original & ~mask) | ((field_value << shift) & mask); return true;
}
