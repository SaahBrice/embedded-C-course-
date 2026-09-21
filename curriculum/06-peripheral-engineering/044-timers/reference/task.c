/* Mission: Schedule with Hardware Timers */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool deadline_reached(uint32_t now, uint32_t deadline) { return (int32_t)(now - deadline) >= 0; }
