/* Mission: Model Memory-Mapped I/O */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool register_update(volatile uint32_t *reg, uint32_t clear_mask, uint32_t set_mask) {
    if (reg == NULL) return false;
    const uint32_t current = *reg;
    *reg = (current & ~clear_mask) | set_mask;
    return true;
}
