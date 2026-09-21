/* Mission: Recognize Undefined Behavior */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool safe_left_shift(uint32_t value, unsigned shift, uint32_t *out_value) {
    if (out_value == NULL || shift >= 32U || value > (UINT32_MAX >> shift)) return false;
    *out_value = value << shift; return true;
}
