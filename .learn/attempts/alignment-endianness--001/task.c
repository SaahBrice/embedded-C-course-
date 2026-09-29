#include "task.h"


bool decode_u32_be(const uint8_t *bytes, size_t length,uint32_t *out_value){
    
    if (bytes == NULL || out_value == NULL || length < 4) return false;
    
    *out_value = (uint32_t)((bytes[0] << 24U) | (bytes[1] << 16U) | (bytes[2] << 8U) | bytes[3]);
    return true;
}