#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(startup_services_ready(true,true,true));assert(!startup_services_ready(true,false,true));assert(queue_absorbs_burst(8U,3U,5U));assert(!queue_absorbs_burst(9U,3U,5U));assert(periodic_load_fits(200U,100U,1000U));assert(!periodic_load_fits(900U,200U,1000U));assert(rtos_partition_justified(3U,true,true));assert(rtos_partition_justified(2U,false,false));assert(!rtos_partition_justified(1U,true,false));assert(!rtos_partition_justified(3U,false,true));
    
    return 0;
}
