/* Mission: Use the Preprocessor Carefully */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

int32_t square_i16_once(int16_t value) { const int32_t widened=value; return widened*widened; }
