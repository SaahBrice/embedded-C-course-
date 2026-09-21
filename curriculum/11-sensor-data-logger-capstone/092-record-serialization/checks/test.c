#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    struct serial_record r={UINT32_C(0x12345678),-2}; uint8_t b[RECORD_WIRE_SIZE]={0U}; assert(record_serialize(&r,b,sizeof b)); const uint8_t expected[]={1U,0x78U,0x56U,0x34U,0x12U,0xfeU,0xffU,0xffU,0xffU}; assert(memcmp(b,expected,sizeof b)==0); assert(!record_serialize(&r,b,8U));
    
    return 0;
}
