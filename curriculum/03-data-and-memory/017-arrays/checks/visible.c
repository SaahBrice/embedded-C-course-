#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_sample_minmax(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define sample_minmax(...) visible_return_sample_minmax("sample_minmax(" #__VA_ARGS__ ")", (sample_minmax)(__VA_ARGS__))

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
    const int16_t v[] = {7, -2, 19, 4}; int16_t low = 0, high = 0; assert(sample_minmax(v, 4U, &low, &high) && low == -2 && high == 19); assert(sample_minmax(v, 1U, &low, &high) && low == 7 && high == 7); assert(!sample_minmax(v, 0U, &low, &high));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
