#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_logger_requirements_valid(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define logger_requirements_valid(...) visible_return_logger_requirements_valid("logger_requirements_valid(" #__VA_ARGS__ ")", (logger_requirements_valid)(__VA_ARGS__))

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
    assert(logger_requirements_valid(1000U,100U,64U)); assert(!logger_requirements_valid(0U,0U,64U)); assert(!logger_requirements_valid(1000U,101U,64U)); assert(!logger_requirements_valid(1000U,50U,1U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
