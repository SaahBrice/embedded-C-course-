/* Mission: Capstone: Validate Samples */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool sample_valid(const struct sensor_sample *sample){return sample!=NULL&&sample->temperature_milli_c>=-40000&&sample->temperature_milli_c<=125000&&sample->humidity_centi_percent<=10000U;}
