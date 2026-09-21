#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_checked_sum(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define checked_sum(...) visible_return_checked_sum("checked_sum(" #__VA_ARGS__ ")", (checked_sum)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 5

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
    const int32_t v[] = {4, 5, 6}; int64_t sum = -1; assert(checked_sum(v, 3U, &sum) && sum == 15); assert(checked_sum(NULL, 0U, &sum) && sum == 0); assert(!checked_sum(NULL, 1U, &sum)); assert(!checked_sum(v, SIZE_MAX, &sum)); assert(!checked_sum(v, 3U, NULL));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
