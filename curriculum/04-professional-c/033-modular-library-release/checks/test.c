#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const uint8_t data[]={1U,2U,3U};assert(crc8_update(0U,1U)==UINT8_C(0x07));assert(crc8(data,3U)==UINT8_C(0x48));assert(crc8(NULL,0U)==0U);assert(crc8_verify(data,3U,UINT8_C(0x48)));assert(!crc8_verify(data,3U,UINT8_C(0x49)));assert(!crc8_verify(NULL,1U,0U));
    
    return 0;
}
