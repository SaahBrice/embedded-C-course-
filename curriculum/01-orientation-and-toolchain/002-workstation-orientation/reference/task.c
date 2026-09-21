/* Mission: Implement Your First Firmware Function */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

int firmware_status(unsigned boot_count) { return boot_count == 0U ? -1 : 0; }
