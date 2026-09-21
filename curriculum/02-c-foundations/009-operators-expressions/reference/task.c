/* Mission: Control Expression Evaluation */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

uint32_t status_bits_update(uint32_t status, uint32_t set_mask, uint32_t clear_mask) { return (status | set_mask) & ~clear_mask; }
