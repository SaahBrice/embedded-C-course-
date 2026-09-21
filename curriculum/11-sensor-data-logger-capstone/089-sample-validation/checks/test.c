#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    struct sensor_sample s={21000,5000U}; assert(sample_valid(&s)); s.temperature_milli_c=-40001; assert(!sample_valid(&s)); s.temperature_milli_c=0;s.humidity_centi_percent=10001U;assert(!sample_valid(&s));assert(!sample_valid(NULL));
    
    return 0;
}
