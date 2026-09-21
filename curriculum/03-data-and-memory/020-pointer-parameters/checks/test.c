#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const uint8_t bytes[] = {0x34U, 0x12U}; uint16_t value = 0U; assert(decode_u16_le(bytes, 2U, &value) && value == UINT16_C(0x1234)); assert(!decode_u16_le(bytes, 1U, &value)); assert(!decode_u16_le(NULL, 2U, &value));
    
    return 0;
}
