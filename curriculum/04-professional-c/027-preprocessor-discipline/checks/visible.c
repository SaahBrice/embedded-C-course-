#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static int32_t visible_return_square_i16_once(const char *call, int32_t value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define square_i16_once(...) visible_return_square_i16_once("square_i16_once(" #__VA_ARGS__ ")", (square_i16_once)(__VA_ARGS__))

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
    assert(square_i16_once(0)==0); assert(square_i16_once(-3)==9); assert(square_i16_once(INT16_MAX)==INT32_C(1073676289)); assert(square_i16_once(INT16_MIN)==INT32_C(1073741824));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
