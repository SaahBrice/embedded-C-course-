#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static enum object_section visible_return_choose_object_section(const char *call, enum object_section value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define choose_object_section(...) visible_return_choose_object_section("choose_object_section(" #__VA_ARGS__ ")", (choose_object_section)(__VA_ARGS__))

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
    assert(choose_object_section(false,true,false)==SECTION_RODATA); assert(choose_object_section(true,true,false)==SECTION_DATA); assert(choose_object_section(true,false,false)==SECTION_BSS); assert(choose_object_section(true,false,true)==SECTION_NOINIT);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
