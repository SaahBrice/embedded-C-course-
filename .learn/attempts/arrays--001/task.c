#include "task.h"




bool sample_minmax(const int16_t *samples, size_t count, int16_t *out_min, int16_t *out_max){

    if(samples == NULL || out_max == NULL || out_min == NULL || count==0) return false;
    int16_t t_sm = samples[0];
    int16_t t_bg = samples[0];
    for(size_t i = 0; i < count; ++i){
        if (samples[i] > t_bg && samples[i] > t_sm){
            t_bg = samples[i];
        } else if (samples[i] < t_bg && samples[i] < t_sm){
            t_sm = samples[i];
        }
    }
    *out_min = t_sm;
    *out_max = t_bg;
    
    return true;
}