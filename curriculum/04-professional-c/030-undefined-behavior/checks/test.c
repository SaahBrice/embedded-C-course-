#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint32_t out = 0U; assert(safe_left_shift(3U,4U,&out) && out == 48U); assert(!safe_left_shift(1U,32U,&out)); assert(!safe_left_shift(UINT32_MAX,1U,&out));
    
    return 0;
}
