#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_logger_record_shape_valid(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define logger_record_shape_valid(...) visible_return_logger_record_shape_valid("logger_record_shape_valid(" #__VA_ARGS__ ")", (logger_record_shape_valid)(__VA_ARGS__))
static uint32_t visible_return_logger_release_checksum(const char *call, uint32_t value) { printf("Call and inputs: %s\n  Actual return: %llu\n", call, (unsigned long long)value); return value; }
#define logger_release_checksum(...) visible_return_logger_release_checksum("logger_release_checksum(" #__VA_ARGS__ ")", (logger_release_checksum)(__VA_ARGS__))
static bool visible_return_logger_release_validate(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define logger_release_validate(...) visible_return_logger_release_validate("logger_release_validate(" #__VA_ARGS__ ")", (logger_release_validate)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 7

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
    const uint8_t record[]={1U,1U,42U};assert(logger_record_shape_valid(record,3U));assert(!logger_record_shape_valid(record,2U));assert(logger_release_checksum(record,3U)==UINT32_C(399283687));assert(logger_release_validate(record,3U,UINT32_C(399283687)));assert(!logger_release_validate(record,3U,0U));const uint8_t wrong[]={2U,1U,42U};assert(!logger_record_shape_valid(wrong,3U));assert(logger_release_checksum(NULL,0U)==UINT32_C(2166136261));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
