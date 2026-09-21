/* Mission: Reason About Scope and Storage */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool instance_increment(unsigned *state) { if (state == NULL || *state == UINT_MAX) return false; ++*state; return true; }
