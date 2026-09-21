/* Mission: Release: Telemetry Converter */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool celsius_in_sensor_range(double c){return c>=-40.0&&c<=125.0;}
bool celsius_to_milli(double c,int32_t *out){if(out==NULL||!celsius_in_sensor_range(c))return false;const double scaled=c*1000.0;*out=(int32_t)(scaled>=0.0?scaled+0.5:scaled-0.5);return true;}
bool telemetry_prepare(double c,bool fault,int32_t *out){return !fault&&celsius_to_milli(c,out);}
