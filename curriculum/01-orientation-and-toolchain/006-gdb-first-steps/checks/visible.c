#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_sample_sum(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define sample_sum(...) visible_return_sample_sum("sample_sum(" #__VA_ARGS__ ")", (sample_sum)(__VA_ARGS__))
static bool visible_return_sample_minimum(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define sample_minimum(...) visible_return_sample_minimum("sample_minimum(" #__VA_ARGS__ ")", (sample_minimum)(__VA_ARGS__))
static bool visible_return_sample_negative_mask(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define sample_negative_mask(...) visible_return_sample_negative_mask("sample_negative_mask(" #__VA_ARGS__ ")", (sample_negative_mask)(__VA_ARGS__))
static bool visible_return_sample_window_analyze(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define sample_window_analyze(...) visible_return_sample_window_analyze("sample_window_analyze(" #__VA_ARGS__ ")", (sample_window_analyze)(__VA_ARGS__))

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
    const int16_t v[]={10,-3,7};int32_t sum=99;int16_t low=99;uint8_t mask=0U;assert(sample_sum(v,3U,&sum)&&sum==14);assert(sample_minimum(v,3U,&low)&&low==-3);assert(sample_negative_mask(v,3U,&mask)&&mask==UINT8_C(0x02));assert(sample_window_analyze(v,3U,&sum,&low,&mask)&&sum==14&&low==-3&&mask==UINT8_C(0x02));assert(!sample_window_analyze(v,0U,&sum,&low,&mask));assert(!sample_window_analyze(v,9U,&sum,&low,&mask));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
