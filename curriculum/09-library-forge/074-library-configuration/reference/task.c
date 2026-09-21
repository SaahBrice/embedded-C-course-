/* Mission: Configure Without Forking */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool queue_config_valid(size_t capacity,bool overwrite_oldest){(void)overwrite_oldest;return capacity>=2U&&capacity<=1024U&&(capacity&(capacity-1U))==0U;}
