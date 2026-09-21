#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint32_t out=0U; assert(datasheet_field_encode(2U,4U,UINT32_C(0x30),&out)&&out==UINT32_C(0x20)); assert(!datasheet_field_encode(4U,4U,UINT32_C(0x30),&out)); assert(!datasheet_field_encode(1U,32U,UINT32_MAX,&out));
    
    return 0;
}
