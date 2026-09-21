#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const uint8_t bytes[]={0x12U,0x34U,0x56U,0x78U}; uint32_t out=0U; assert(decode_u32_be(bytes,4U,&out)&&out==UINT32_C(0x12345678)); assert(!decode_u32_be(bytes,3U,&out)); assert(!decode_u32_be(NULL,4U,&out));
    
    return 0;
}
