#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_sample_valid(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define sample_valid(...) visible_return_sample_valid("sample_valid(" #__VA_ARGS__ ")", (sample_valid)(__VA_ARGS__))

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
    struct sensor_sample s={21000,5000U}; assert(sample_valid(&s)); s.temperature_milli_c=-40001; assert(!sample_valid(&s)); s.temperature_milli_c=0;s.humidity_centi_percent=10001U;assert(!sample_valid(&s));assert(!sample_valid(NULL));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
