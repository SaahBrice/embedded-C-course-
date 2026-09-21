/* Mission: Drive Digital I/O */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool gpio_output_level(bool command_on, bool active_low) { return active_low ? !command_on : command_on; }
