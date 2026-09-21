#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const uint8_t good[]={1U,2U,0x34U,0x12U};uint16_t value=0U;struct parsed_packet out={9U,9U};assert(packet_header_valid(good,4U));assert(packet_decode_value(good,4U,&value)&&value==UINT16_C(0x1234));assert(packet_parse(good,4U,&out)&&out.kind==1U&&out.value==UINT16_C(0x1234));const uint8_t bad[]={2U,2U,0U,0U};assert(!packet_header_valid(bad,4U));assert(!packet_parse(good,3U,&out));
    
    return 0;
}
