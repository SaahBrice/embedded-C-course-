#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_register_field_write(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define register_field_write(...) visible_return_register_field_write("register_field_write(" #__VA_ARGS__ ")", (register_field_write)(__VA_ARGS__))

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
    uint32_t out = 0U; assert(register_field_write(UINT32_C(0xa5a5000f),UINT32_C(0x70),4U,5U,&out)); assert(out == UINT32_C(0xa5a5005f)); assert(!register_field_write(0U,UINT32_C(0x70),4U,8U,&out)); assert(!register_field_write(0U,0U,0U,0U,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
