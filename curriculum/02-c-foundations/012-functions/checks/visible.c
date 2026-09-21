#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static int32_t visible_return_clamp_i32(const char *call, int32_t value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define clamp_i32(...) visible_return_clamp_i32("clamp_i32(" #__VA_ARGS__ ")", (clamp_i32)(__VA_ARGS__))

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
    assert(clamp_i32(5, 0, 10) == 5); assert(clamp_i32(-1, 0, 10) == 0); assert(clamp_i32(11, 0, 10) == 10); assert(clamp_i32(4, 7, 3) == 7);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
