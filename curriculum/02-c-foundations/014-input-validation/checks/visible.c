#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_parse_u16(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define parse_u16(...) visible_return_parse_u16("parse_u16(" #__VA_ARGS__ ")", (parse_u16)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 6

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
    uint16_t value = 9U; assert(parse_u16("0", &value) && value == 0U); assert(parse_u16("65535", &value) && value == 65535U); assert(!parse_u16("65536", &value)); assert(!parse_u16("-1", &value)); assert(!parse_u16("12x", &value)); assert(!parse_u16("", &value));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
