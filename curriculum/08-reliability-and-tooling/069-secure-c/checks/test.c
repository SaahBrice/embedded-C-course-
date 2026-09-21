#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const uint8_t good[]={1U,2U,0xaaU,0xbbU}; size_t out=0U; assert(frame_payload_length(good,4U,&out)&&out==2U); const uint8_t bad[]={1U,9U}; assert(!frame_payload_length(bad,2U,&out)); assert(!frame_payload_length(good,1U,&out));
    
    return 0;
}
