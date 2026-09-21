#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(saturating_counter_add(10U,20U) == 30U); assert(saturating_counter_add(UINT32_MAX-1U,2U) == UINT32_MAX); assert(saturating_counter_add(UINT32_MAX,0U) == UINT32_MAX);
    
    return 0;
}
