#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_ring_state_valid(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define ring_state_valid(...) visible_return_ring_state_valid("ring_state_valid(" #__VA_ARGS__ ")", (ring_state_valid)(__VA_ARGS__))

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
    assert(ring_state_valid(0U,0U,0U,4U)); assert(ring_state_valid(0U,0U,4U,4U)); assert(ring_state_valid(3U,1U,2U,4U)); assert(!ring_state_valid(4U,0U,0U,4U)); assert(!ring_state_valid(0U,0U,1U,0U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
