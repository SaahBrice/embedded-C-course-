#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_temperature_fits_i16(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define temperature_fits_i16(...) visible_return_temperature_fits_i16("temperature_fits_i16(" #__VA_ARGS__ ")", (temperature_fits_i16)(__VA_ARGS__))

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
    assert(temperature_fits_i16(INT16_MIN)); assert(temperature_fits_i16(INT16_MAX)); assert(!temperature_fits_i16((int32_t)INT16_MIN-1)); assert(!temperature_fits_i16((int32_t)INT16_MAX+1));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
