#include "task.h"




bool scale_offset_sample(int32_t raw, int32_t offset, int32_t scale, int32_t *out_value){

    if (out_value==NULL || raw >= INT32_MAX ||offset >= INT32_MAX) return false;

    int64_t results = 0;
    results = (int64_t)(raw+offset) * (int64_t)scale;
    if ((int32_t)results > INT32_MAX || (int32_t)results < INT32_MIN) return false;
    *out_value = (int32_t)results;
    return true;

}