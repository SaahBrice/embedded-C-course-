#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_adc_to_millivolts(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define adc_to_millivolts(...) visible_return_adc_to_millivolts("adc_to_millivolts(" #__VA_ARGS__ ")", (adc_to_millivolts)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 4

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
    uint16_t mv = 99U; assert(adc_to_millivolts(0U, 3300U, &mv) && mv == 0U);
assert(adc_to_millivolts(4095U, 3300U, &mv) && mv == 3300U);
assert(!adc_to_millivolts(4096U, 3300U, &mv)); assert(!adc_to_millivolts(1U, 0U, &mv));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
