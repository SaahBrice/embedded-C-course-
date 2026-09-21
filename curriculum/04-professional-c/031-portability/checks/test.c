#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const uint8_t b[] = {0x78U,0x56U,0x34U,0x12U}; uint32_t out = 0U; assert(read_u32_le(b,4U,&out) && out == UINT32_C(0x12345678)); assert(!read_u32_le(b,3U,&out));
    
    return 0;
}
