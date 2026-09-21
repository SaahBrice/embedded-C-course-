#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(swap_nibbles(UINT8_C(0xa5))==UINT8_C(0x5a)); assert(swap_nibbles(UINT8_C(0xf0))==UINT8_C(0x0f)); assert(swap_nibbles(0U)==0U);
    
    return 0;
}
