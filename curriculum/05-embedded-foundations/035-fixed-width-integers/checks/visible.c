#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static uint32_t visible_return_saturating_counter_add(const char *call, uint32_t value) { printf("Call and inputs: %s\n  Actual return: %llu\n", call, (unsigned long long)value); return value; }
#define saturating_counter_add(...) visible_return_saturating_counter_add("saturating_counter_add(" #__VA_ARGS__ ")", (saturating_counter_add)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 3

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
    assert(saturating_counter_add(10U,20U) == 30U); assert(saturating_counter_add(UINT32_MAX-1U,2U) == UINT32_MAX); assert(saturating_counter_add(UINT32_MAX,0U) == UINT32_MAX);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
