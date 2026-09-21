/* Mission: Use Host Sanitizers */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool copy_samples(int16_t *destination, size_t capacity, const int16_t *source, size_t count) {
    if ((destination == NULL || source == NULL) && count != 0U) return false;
    if (count > capacity) return false;
    if (count != 0U) memmove(destination,source,count*sizeof *source);
    return true;
}
