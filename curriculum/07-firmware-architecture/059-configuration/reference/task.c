/* Mission: Make Configuration Explicit */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool controller_config_valid(uint32_t sample_period_ms,int32_t low_limit,int32_t high_limit){return sample_period_ms!=0U&&sample_period_ms<=UINT32_C(60000)&&low_limit<=high_limit;}
