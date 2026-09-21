#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_counter_add_bounded(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define counter_add_bounded(...) visible_return_counter_add_bounded("counter_add_bounded(" #__VA_ARGS__ ")", (counter_add_bounded)(__VA_ARGS__))

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
    unsigned out=0U; assert(counter_add_bounded(3U,4U,10U,&out)&&out==7U); assert(counter_add_bounded(10U,0U,10U,&out)&&out==10U); assert(!counter_add_bounded(9U,2U,10U,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
