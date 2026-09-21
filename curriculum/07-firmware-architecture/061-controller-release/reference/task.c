/* Mission: Release: Portable Sensor Controller */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool sensor_controller_due(const struct sensor_controller *c,uint32_t now){return c!=NULL&&c->period!=0U&&(uint32_t)(now-c->last_sample)>=c->period;}
bool sensor_sample_acceptable(bool ready,int32_t value,int32_t minimum,int32_t maximum){return ready&&minimum<=maximum&&value>=minimum&&value<=maximum;}
bool sensor_controller_update(struct sensor_controller *c,uint32_t now,bool ready){if(!sensor_controller_due(c,now)||!ready)return false;c->last_sample+=c->period;++c->samples;return true;}
