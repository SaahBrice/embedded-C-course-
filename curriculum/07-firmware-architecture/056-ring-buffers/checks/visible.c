#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_byte_ring_push(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define byte_ring_push(...) visible_return_byte_ring_push("byte_ring_push(" #__VA_ARGS__ ")", (byte_ring_push)(__VA_ARGS__))
static bool visible_return_byte_ring_pop(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define byte_ring_pop(...) visible_return_byte_ring_pop("byte_ring_pop(" #__VA_ARGS__ ")", (byte_ring_pop)(__VA_ARGS__))

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
    struct byte_ring r={{0U},0U,0U,0U}; uint8_t out=0U; assert(!byte_ring_pop(&r,&out)); for(uint8_t i=1U;i<=4U;++i) assert(byte_ring_push(&r,i)); assert(!byte_ring_push(&r,5U)); assert(byte_ring_pop(&r,&out)&&out==1U); assert(byte_ring_push(&r,5U)); for(uint8_t i=2U;i<=5U;++i) assert(byte_ring_pop(&r,&out)&&out==i);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
