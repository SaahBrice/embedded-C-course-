#include "task.h"
#include "sim_adc.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_adc_code_to_mv(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define adc_code_to_mv(...) visible_return_adc_code_to_mv("adc_code_to_mv(" #__VA_ARGS__ ")", (adc_code_to_mv)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 7

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
    uint16_t mv=0U; assert(adc_code_to_mv(2048U,12U,3300U,&mv) && mv==1650U); assert(adc_code_to_mv(4095U,12U,3300U,&mv) && mv==3300U); assert(!adc_code_to_mv(4096U,12U,3300U,&mv));
    uint16_t raw=0U,scaled=0U; sim_adc_reset(); assert(sim_adc_set(2U,2048U)==SIM_ADC_OK); assert(sim_adc_read(2U,&raw)==SIM_ADC_OK); assert(adc_code_to_mv(raw,12U,3300U,&scaled)&&scaled==1650U); assert(sim_adc_set(2U,4096U)==SIM_ADC_RANGE);
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
