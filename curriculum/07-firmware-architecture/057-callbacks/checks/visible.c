#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>

static bool capture_status(void *context,uint8_t value){*(unsigned *)context += value;return true;}

static bool visible_return_callback_run_once(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define callback_run_once(...) visible_return_callback_run_once("callback_run_once(" #__VA_ARGS__ ")", (callback_run_once)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 2

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
    unsigned total=1U; assert(callback_run_once(capture_status,&total,4U)&&total==5U); assert(!callback_run_once(NULL,&total,3U)&&total==5U);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
