#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static enum measurement_action visible_return_classify_measurement(const char *call, enum measurement_action value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define classify_measurement(...) visible_return_classify_measurement("classify_measurement(" #__VA_ARGS__ ")", (classify_measurement)(__VA_ARGS__))

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
    assert(classify_measurement(20000, false) == ACTION_ACCEPT); assert(classify_measurement(-40001, false) == ACTION_RETRY); assert(classify_measurement(125001, false) == ACTION_RETRY); assert(classify_measurement(20000, true) == ACTION_SHUTDOWN);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
