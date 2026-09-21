#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const uint8_t record[]={1U,1U,42U};assert(logger_record_shape_valid(record,3U));assert(!logger_record_shape_valid(record,2U));assert(logger_release_checksum(record,3U)==UINT32_C(399283687));assert(logger_release_validate(record,3U,UINT32_C(399283687)));assert(!logger_release_validate(record,3U,0U));const uint8_t wrong[]={2U,1U,42U};assert(!logger_record_shape_valid(wrong,3U));assert(logger_release_checksum(NULL,0U)==UINT32_C(2166136261));
    
    return 0;
}
