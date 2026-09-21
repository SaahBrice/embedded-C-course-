#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_record_ring_push(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define record_ring_push(...) visible_return_record_ring_push("record_ring_push(" #__VA_ARGS__ ")", (record_ring_push)(__VA_ARGS__))
static bool visible_return_record_ring_pop(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define record_ring_pop(...) visible_return_record_ring_pop("record_ring_pop(" #__VA_ARGS__ ")", (record_ring_pop)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 5

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
    struct record_ring q={{{0U,0}},0U,0U,0U}; struct log_record out={0U,0}; for(int32_t i=1;i<=3;++i)assert(record_ring_push(&q,(struct log_record){(uint32_t)i,i}));assert(!record_ring_push(&q,(struct log_record){4U,4}));assert(record_ring_pop(&q,&out)&&out.value==1);assert(record_ring_push(&q,(struct log_record){4U,4}));for(int32_t i=2;i<=4;++i)assert(record_ring_pop(&q,&out)&&out.value==i);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
