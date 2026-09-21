#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(temperature_fits_i16(INT16_MIN)); assert(temperature_fits_i16(INT16_MAX)); assert(!temperature_fits_i16((int32_t)INT16_MIN-1)); assert(!temperature_fits_i16((int32_t)INT16_MAX+1));
    
    return 0;
}
