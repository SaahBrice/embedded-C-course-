#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_sample_average(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define sample_average(...) visible_return_sample_average("sample_average(" #__VA_ARGS__ ")", (sample_average)(__VA_ARGS__))

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
    const int16_t v[] = {3, 6, 9, 12}; int32_t avg = 0; assert(sample_average(v, 4U, &avg) && avg == 7); assert(!sample_average(v, 0U, &avg)); assert(!sample_average(NULL, 1U, &avg));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
