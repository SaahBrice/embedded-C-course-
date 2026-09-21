#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_bounded_copy(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define bounded_copy(...) visible_return_bounded_copy("bounded_copy(" #__VA_ARGS__ ")", (bounded_copy)(__VA_ARGS__))

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
    uint8_t d[4] = {0U}; const uint8_t s[] = {1U,2U,3U}; assert(bounded_copy(d,4U,s,3U) && d[2] == 3U); assert(!bounded_copy(d,2U,s,3U)); assert(bounded_copy(NULL,0U,NULL,0U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
