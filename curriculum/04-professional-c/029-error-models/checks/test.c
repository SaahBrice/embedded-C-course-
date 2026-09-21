#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    int32_t out = -1; assert(sensor_scale(5U,10U,&out) == SCALE_OK && out == 500); assert(sensor_scale(11U,10U,&out) == SCALE_RANGE); assert(sensor_scale(1U,0U,&out) == SCALE_ARGUMENT);
    
    return 0;
}
