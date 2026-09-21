#include "task.h"
#include "sim_pwm.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_pwm_compare(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define pwm_compare(...) visible_return_pwm_compare("pwm_compare(" #__VA_ARGS__ ")", (pwm_compare)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 8

static unsigned visible_case_number;
static unsigned visible_failures;

static void visible_check(int passed, const char *expression) {
    printf("Case %u\n  Expected condition: %s\n  Observed condition: %s\n  Result: %s\n",
           visible_case_number, expression, passed ? "true" : "false",
           passed ? "PASS" : "FAIL");
    if (!passed) ++visible_failures;
}

#define assert(expression) do {     ++visible_case_number;     visible_check(!!(expression), #expression); } while (0)

int main(void) {
    uint32_t compare=0U; assert(pwm_compare(1000U,0U,&compare)&&compare==0U); assert(pwm_compare(1000U,25U,&compare)&&compare==250U); assert(pwm_compare(UINT32_MAX,100U,&compare)&&compare==UINT32_MAX); assert(!pwm_compare(10U,101U,&compare));
    uint32_t calculated=0U,period=0U,observed=0U; sim_pwm_reset(); assert(pwm_compare(1000U,25U,&calculated)); assert(sim_pwm_configure(0U,1000U,calculated)==SIM_PWM_OK); assert(sim_pwm_observe(0U,&period,&observed)==SIM_PWM_OK&&period==1000U&&observed==250U); assert(sim_pwm_configure(0U,10U,11U)==SIM_PWM_ARGUMENT);
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
