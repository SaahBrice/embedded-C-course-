/* Mission: Reason About Shared State */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool sequence_is_newer(uint32_t candidate,uint32_t current){const uint32_t distance=candidate-current;return distance!=0U&&distance<UINT32_C(0x80000000);}
