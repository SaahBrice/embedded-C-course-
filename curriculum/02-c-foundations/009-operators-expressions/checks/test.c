#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(status_bits_update(UINT32_C(0x0a), UINT32_C(0x05), UINT32_C(0x08)) == UINT32_C(0x07)); assert(status_bits_update(UINT32_MAX, 0U, UINT32_MAX) == 0U);
    
    return 0;
}
