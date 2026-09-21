#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_buffer_append(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define buffer_append(...) visible_return_buffer_append("buffer_append(" #__VA_ARGS__ ")", (buffer_append)(__VA_ARGS__))

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
    char a[8] = "AB"; assert(buffer_append(a, sizeof a, "CDE") && strcmp(a, "ABCDE") == 0);
char b[5] = "AB"; assert(!buffer_append(b, sizeof b, "CDE") && strcmp(b, "AB") == 0);
char c[1] = {0}; assert(buffer_append(c, sizeof c, "") && c[0] == '\0');
char d[3] = {'A','B','C'}; assert(!buffer_append(d, sizeof d, "x"));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
