#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(!watchdog_elapsed(109U,100U,10U));assert(watchdog_elapsed(110U,100U,10U));assert(watchdog_elapsed(3U,UINT32_MAX-5U,8U));assert(ring_indices_valid(3U,1U,2U,4U));assert(!ring_indices_valid(4U,0U,0U,4U));assert(!recovery_required(false,true,2U,3U));assert(recovery_required(true,true,0U,3U));assert(recovery_required(false,false,0U,3U));assert(recovery_required(false,true,3U,3U));
    
    return 0;
}
