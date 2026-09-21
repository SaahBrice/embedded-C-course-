#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint32_t out = 0U; assert(register_field_write(UINT32_C(0xa5a5000f),UINT32_C(0x70),4U,5U,&out)); assert(out == UINT32_C(0xa5a5005f)); assert(!register_field_write(0U,UINT32_C(0x70),4U,8U,&out)); assert(!register_field_write(0U,0U,0U,0U,&out));
    
    return 0;
}
