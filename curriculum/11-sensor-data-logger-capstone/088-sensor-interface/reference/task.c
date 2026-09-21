/* Mission: Capstone: Sensor Port */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

enum sensor_status sensor_read_checked(sensor_read_fn read,void *context,int32_t minimum,int32_t maximum,int32_t *out_value){if(read==NULL||out_value==NULL||minimum>maximum)return SENSOR_UNAVAILABLE;int32_t value=0;enum sensor_status status=read(context,&value);if(status!=SENSOR_OK)return status;if(value<minimum||value>maximum)return SENSOR_RANGE;*out_value=value;return SENSOR_OK;}
