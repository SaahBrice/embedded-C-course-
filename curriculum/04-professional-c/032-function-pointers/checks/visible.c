#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>

static bool capture_handler(void *context,uint8_t value){*(unsigned *)context += value;return true;}

static bool visible_return_event_dispatch(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define event_dispatch(...) visible_return_event_dispatch("event_dispatch(" #__VA_ARGS__ ")", (event_dispatch)(__VA_ARGS__))

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
    event_handler handlers[] = {capture_handler, NULL}; unsigned total = 0U;
assert(event_dispatch(0U,handlers,2U,&total,7U) && total == 7U); assert(!event_dispatch(1U,handlers,2U,&total,1U)); assert(!event_dispatch(2U,handlers,2U,&total,1U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
