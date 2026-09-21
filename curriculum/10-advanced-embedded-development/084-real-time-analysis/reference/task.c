/* Mission: Analyze Real-Time Schedulability */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool nonpreemptive_deadline_met(uint32_t wcet_us,uint32_t blocking_us,uint32_t period_us){return wcet_us<=period_us&&blocking_us<=period_us-wcet_us;}
