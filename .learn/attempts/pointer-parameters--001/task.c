#include "task.h"

bool decode_u16_le(const uint8_t *bytes, size_t length, uint16_t *out_value){
    if (bytes == NULL || out_value == NULL || length < 2U) return false;

    *out_value = (uint16_t)(bytes[0] | (bytes[1]<< 8));

    return true;
}