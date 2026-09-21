#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_region_contains(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define region_contains(...) visible_return_region_contains("region_contains(" #__VA_ARGS__ ")", (region_contains)(__VA_ARGS__))

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
    assert(region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x20000000),16U)); assert(region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x200003f0),16U)); assert(!region_contains(UINT32_C(0x20000000),1024U,UINT32_C(0x1fffffff),1U)); assert(!region_contains(UINT32_C(0xfffffff0),32U,UINT32_C(0xfffffff0),32U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
