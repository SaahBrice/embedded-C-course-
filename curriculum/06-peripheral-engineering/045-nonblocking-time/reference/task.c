/* Mission: Replace Blocking Delays */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool blinker_update(struct blinker *blinker, uint32_t now) {
    if (blinker == NULL || blinker->period == 0U) return false;
    if ((uint32_t)(now - blinker->last_change) < blinker->period) return false;
    blinker->last_change += blinker->period; blinker->level = !blinker->level; return true;
}
