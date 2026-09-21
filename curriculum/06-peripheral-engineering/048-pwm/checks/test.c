#include "task.h"
#include "sim_pwm.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint32_t compare=0U; assert(pwm_compare(1000U,0U,&compare)&&compare==0U); assert(pwm_compare(1000U,25U,&compare)&&compare==250U); assert(pwm_compare(UINT32_MAX,100U,&compare)&&compare==UINT32_MAX); assert(!pwm_compare(10U,101U,&compare));
    uint32_t calculated=0U,period=0U,observed=0U; sim_pwm_reset(); assert(pwm_compare(1000U,25U,&calculated)); assert(sim_pwm_configure(0U,1000U,calculated)==SIM_PWM_OK); assert(sim_pwm_observe(0U,&period,&observed)==SIM_PWM_OK&&period==1000U&&observed==250U); assert(sim_pwm_configure(0U,10U,11U)==SIM_PWM_ARGUMENT);
    return 0;
}
