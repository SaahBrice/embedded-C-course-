#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const int16_t v[]={10,-3,7};int32_t sum=99;int16_t low=99;uint8_t mask=0U;assert(sample_sum(v,3U,&sum)&&sum==14);assert(sample_minimum(v,3U,&low)&&low==-3);assert(sample_negative_mask(v,3U,&mask)&&mask==UINT8_C(0x02));assert(sample_window_analyze(v,3U,&sum,&low,&mask)&&sum==14&&low==-3&&mask==UINT8_C(0x02));assert(!sample_window_analyze(v,0U,&sum,&low,&mask));assert(!sample_window_analyze(v,9U,&sum,&low,&mask));
    
    return 0;
}
