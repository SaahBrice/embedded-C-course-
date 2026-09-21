#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_volts_to_millivolts(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define volts_to_millivolts(...) visible_return_volts_to_millivolts("volts_to_millivolts(" #__VA_ARGS__ ")", (volts_to_millivolts)(__VA_ARGS__))

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
    uint32_t out=9U; assert(volts_to_millivolts(3.3,&out)&&out==3300U); assert(volts_to_millivolts(0.0006,&out)&&out==1U); assert(!volts_to_millivolts(-0.1,&out)); assert(!volts_to_millivolts(70.0,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
