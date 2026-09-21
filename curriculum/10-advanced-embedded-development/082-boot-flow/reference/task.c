/* Mission: Design a Safe Boot Flow */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

enum boot_phase boot_next(enum boot_phase current,bool step_ok){if(!step_ok||current>=BOOT_READY)return BOOT_SAFE_OUTPUTS;return (enum boot_phase)(current+1);}
