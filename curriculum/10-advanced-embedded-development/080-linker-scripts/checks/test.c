#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x20000000),16U)); assert(region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x200003f0),16U)); assert(!region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x1fffffff),1U)); assert(!region_contains(UINT32_C(0xfffffff0),32U,UINT32_C(0xfffffff0),32U));
    
    return 0;
}
