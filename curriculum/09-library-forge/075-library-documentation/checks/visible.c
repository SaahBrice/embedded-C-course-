#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_documented_copy(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define documented_copy(...) visible_return_documented_copy("documented_copy(" #__VA_ARGS__ ")", (documented_copy)(__VA_ARGS__))

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
    uint8_t out[3]={0}; const uint8_t in[]={1U,2U,3U}; assert(documented_copy(out,3U,in,3U)&&out[2]==3U); assert(!documented_copy(out,2U,in,3U)); assert(documented_copy(NULL,0U,NULL,0U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
