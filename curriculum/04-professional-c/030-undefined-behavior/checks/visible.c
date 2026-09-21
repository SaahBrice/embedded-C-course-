#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_safe_left_shift(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define safe_left_shift(...) visible_return_safe_left_shift("safe_left_shift(" #__VA_ARGS__ ")", (safe_left_shift)(__VA_ARGS__))

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
    uint32_t out = 0U; assert(safe_left_shift(3U,4U,&out) && out == 48U); assert(!safe_left_shift(1U,32U,&out)); assert(!safe_left_shift(UINT32_MAX,1U,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
