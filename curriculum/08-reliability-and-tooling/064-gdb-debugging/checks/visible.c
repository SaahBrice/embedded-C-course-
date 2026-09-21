#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static size_t visible_return_replace_value(const char *call, size_t value) { printf("Call and inputs: %s\n  Actual return: %llu\n", call, (unsigned long long)value); return value; }
#define replace_value(...) visible_return_replace_value("replace_value(" #__VA_ARGS__ ")", (replace_value)(__VA_ARGS__))

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
    int32_t v[]={1,2,1,3}; assert(replace_value(v,4U,1,9)==2U); assert(v[0]==9&&v[1]==2&&v[2]==9&&v[3]==3); assert(replace_value(v,0U,9,0)==0U); assert(replace_value(NULL,4U,1,2)==0U);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
