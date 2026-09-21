#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint16_t mv = 99U; assert(adc_to_millivolts(0U, 3300U, &mv) && mv == 0U);
assert(adc_to_millivolts(4095U, 3300U, &mv) && mv == 3300U);
assert(!adc_to_millivolts(4096U, 3300U, &mv)); assert(!adc_to_millivolts(1U, 0U, &mv));
    
    return 0;
}
