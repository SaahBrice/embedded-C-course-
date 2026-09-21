#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(sequence_is_newer(11U,10U)); assert(!sequence_is_newer(10U,10U)); assert(sequence_is_newer(0U,UINT32_MAX)); assert(!sequence_is_newer(UINT32_C(0x80000000),0U));
    
    return 0;
}
