#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    struct sensor_controller c={10U,100U,0U};assert(!sensor_controller_due(&c,109U));assert(sensor_controller_due(&c,110U));assert(sensor_sample_acceptable(true,25,-40,125));assert(!sensor_sample_acceptable(false,25,-40,125));assert(!sensor_sample_acceptable(true,126,-40,125));assert(sensor_controller_update(&c,110U,true)&&c.samples==1U&&c.last_sample==110U);assert(!sensor_controller_update(&c,120U,false));
    
    return 0;
}
