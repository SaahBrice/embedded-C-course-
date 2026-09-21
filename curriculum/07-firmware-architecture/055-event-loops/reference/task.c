/* Mission: Build a Cooperative Event Loop */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool task_due(uint32_t now, uint32_t last_run, uint32_t period) { return period != 0U && (uint32_t)(now - last_run) >= period; }
