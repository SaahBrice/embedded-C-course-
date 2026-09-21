#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(boot_next(BOOT_SAFE_OUTPUTS,true)==BOOT_CLOCKS); assert(boot_next(BOOT_DRIVERS,true)==BOOT_ENABLE_ACTUATORS); assert(boot_next(BOOT_CLOCKS,false)==BOOT_SAFE_OUTPUTS); assert(boot_next(BOOT_READY,true)==BOOT_SAFE_OUTPUTS);
    
    return 0;
}
