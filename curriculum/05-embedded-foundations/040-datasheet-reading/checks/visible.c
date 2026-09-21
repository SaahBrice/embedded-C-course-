#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_datasheet_field_encode(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define datasheet_field_encode(...) visible_return_datasheet_field_encode("datasheet_field_encode(" #__VA_ARGS__ ")", (datasheet_field_encode)(__VA_ARGS__))

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
    uint32_t out=0U; assert(datasheet_field_encode(2U,4U,UINT32_C(0x30),&out)&&out==UINT32_C(0x20)); assert(!datasheet_field_encode(4U,4U,UINT32_C(0x30),&out)); assert(!datasheet_field_encode(1U,32U,UINT32_MAX,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
