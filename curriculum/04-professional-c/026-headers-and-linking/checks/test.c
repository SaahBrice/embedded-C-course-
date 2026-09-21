#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(crc8_update(0U, 0U) == 0U); assert(crc8_update(0U, UINT8_C(0x31)) == UINT8_C(0x97)); assert(crc8_update(UINT8_C(0x5a), UINT8_C(0xc3)) == UINT8_C(0xc6));
    
    return 0;
}
