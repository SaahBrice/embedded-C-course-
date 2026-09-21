/* Mission: Prevent Lifetime Defects */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool snapshot_i16(const int16_t *source, int16_t *destination) { if (source==NULL||destination==NULL) return false; *destination=*source; return true; }
