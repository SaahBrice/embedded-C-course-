#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint32_t out=9U; assert(volts_to_millivolts(3.3,&out)&&out==3300U); assert(volts_to_millivolts(0.0006,&out)&&out==1U); assert(!volts_to_millivolts(-0.1,&out)); assert(!volts_to_millivolts(70.0,&out));
    
    return 0;
}
