#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(load_modify_value(UINT32_C(0xf0),UINT32_C(0x05),UINT32_C(0x30))==UINT32_C(0xc5)); assert(load_modify_value(0U,UINT32_C(0x80),0U)==UINT32_C(0x80));
    
    return 0;
}
