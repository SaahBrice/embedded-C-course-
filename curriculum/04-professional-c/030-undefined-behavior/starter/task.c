#include "task.h"
bool safe_left_shift(uint32_t value, unsigned shift, uint32_t *out_value) { *out_value = value << shift; return true; }
