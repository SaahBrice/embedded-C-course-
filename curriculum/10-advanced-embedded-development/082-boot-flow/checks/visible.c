#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static enum boot_phase visible_return_boot_next(const char *call, enum boot_phase value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define boot_next(...) visible_return_boot_next("boot_next(" #__VA_ARGS__ ")", (boot_next)(__VA_ARGS__))

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
    assert(boot_next(BOOT_SAFE_OUTPUTS,true)==BOOT_CLOCKS); assert(boot_next(BOOT_DRIVERS,true)==BOOT_ENABLE_ACTUATORS); assert(boot_next(BOOT_CLOCKS,false)==BOOT_SAFE_OUTPUTS); assert(boot_next(BOOT_READY,true)==BOOT_SAFE_OUTPUTS);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
