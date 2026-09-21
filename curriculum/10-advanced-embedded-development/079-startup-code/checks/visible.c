#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_zero_bss_words(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define zero_bss_words(...) visible_return_zero_bss_words("zero_bss_words(" #__VA_ARGS__ ")", (zero_bss_words)(__VA_ARGS__))

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
    uint32_t words[]={1U,2U,3U}; assert(zero_bss_words(words,3U)&&words[0]==0U&&words[2]==0U); assert(zero_bss_words(NULL,0U)); assert(!zero_bss_words(NULL,1U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
