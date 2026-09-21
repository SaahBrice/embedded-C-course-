#include "task.h"
#include "sim_adc.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint16_t mv=0U; assert(adc_code_to_mv(2048U,12U,3300U,&mv) && mv==1650U); assert(adc_code_to_mv(4095U,12U,3300U,&mv) && mv==3300U); assert(!adc_code_to_mv(4096U,12U,3300U,&mv));
    uint16_t raw=0U,scaled=0U; sim_adc_reset(); assert(sim_adc_set(2U,2048U)==SIM_ADC_OK); assert(sim_adc_read(2U,&raw)==SIM_ADC_OK); assert(adc_code_to_mv(raw,12U,3300U,&scaled)&&scaled==1650U); assert(sim_adc_set(2U,4096U)==SIM_ADC_RANGE);
    return 0;
}
