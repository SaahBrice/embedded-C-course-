#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(firmware_status(0U) == -1); assert(firmware_status(1U) == 0); assert(firmware_status(42U) == 0);
    
    return 0;
}
