#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static enum controller_state visible_return_controller_transition(const char *call, enum controller_state value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define controller_transition(...) visible_return_controller_transition("controller_transition(" #__VA_ARGS__ ")", (controller_transition)(__VA_ARGS__))

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
    assert(controller_transition(CONTROLLER_IDLE,EVENT_START)==CONTROLLER_SAMPLING); assert(controller_transition(CONTROLLER_SAMPLING,EVENT_SAMPLE_OK)==CONTROLLER_IDLE); assert(controller_transition(CONTROLLER_SAMPLING,EVENT_SAMPLE_BAD)==CONTROLLER_FAULT); assert(controller_transition(CONTROLLER_FAULT,EVENT_RESET)==CONTROLLER_IDLE); assert(controller_transition((enum controller_state)99,EVENT_RESET)==CONTROLLER_FAULT);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
