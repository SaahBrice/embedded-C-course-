#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    int32_t v=77;assert(celsius_in_sensor_range(-40.0));assert(!celsius_in_sensor_range(125.1));assert(celsius_to_milli(21.125,&v)&&v==21125);assert(celsius_to_milli(-0.0006,&v)&&v==-1);v=77;assert(telemetry_prepare(3.3,false,&v)&&v==3300);assert(!telemetry_prepare(3.3,true,&v)&&v==3300);
    
    return 0;
}
