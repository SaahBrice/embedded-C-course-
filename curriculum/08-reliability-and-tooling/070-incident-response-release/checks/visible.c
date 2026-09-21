#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_watchdog_elapsed(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define watchdog_elapsed(...) visible_return_watchdog_elapsed("watchdog_elapsed(" #__VA_ARGS__ ")", (watchdog_elapsed)(__VA_ARGS__))
static bool visible_return_ring_indices_valid(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define ring_indices_valid(...) visible_return_ring_indices_valid("ring_indices_valid(" #__VA_ARGS__ ")", (ring_indices_valid)(__VA_ARGS__))
static bool visible_return_recovery_required(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define recovery_required(...) visible_return_recovery_required("recovery_required(" #__VA_ARGS__ ")", (recovery_required)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 9

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
    assert(!watchdog_elapsed(109U,100U,10U));assert(watchdog_elapsed(110U,100U,10U));assert(watchdog_elapsed(3U,UINT32_MAX-5U,8U));assert(ring_indices_valid(3U,1U,2U,4U));assert(!ring_indices_valid(4U,0U,0U,4U));assert(!recovery_required(false,true,2U,3U));assert(recovery_required(true,true,0U,3U));assert(recovery_required(false,false,0U,3U));assert(recovery_required(false,true,3U,3U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
