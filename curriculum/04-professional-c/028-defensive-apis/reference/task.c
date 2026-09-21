/* Mission: Design Defensive APIs */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool bounded_copy(uint8_t *destination, size_t capacity, const uint8_t *source, size_t count) {
    if ((destination == NULL && count != 0U) || (source == NULL && count != 0U) || count > capacity) return false;
    if (count != 0U) memmove(destination, source, count);
    return true;
}
