#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_elf_header_targets_arm(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define elf_header_targets_arm(...) visible_return_elf_header_targets_arm("elf_header_targets_arm(" #__VA_ARGS__ ")", (elf_header_targets_arm)(__VA_ARGS__))

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
    const uint8_t arm[20]={0x7fU,'E','L','F',0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0x28U,0U}; assert(elf_header_targets_arm(arm,20U)); assert(!elf_header_targets_arm(arm,19U)); uint8_t host[20]={0}; memcpy(host,arm,20U); host[18]=0x3eU; assert(!elf_header_targets_arm(host,20U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
