#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static size_t visible_return_record_queue_required_bytes(const char *call, size_t value) { printf("Call and inputs: %s\n  Actual return: %llu\n", call, (unsigned long long)value); return value; }
#define record_queue_required_bytes(...) visible_return_record_queue_required_bytes("record_queue_required_bytes(" #__VA_ARGS__ ")", (record_queue_required_bytes)(__VA_ARGS__))
static bool visible_return_record_queue_init(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define record_queue_init(...) visible_return_record_queue_init("record_queue_init(" #__VA_ARGS__ ")", (record_queue_init)(__VA_ARGS__))
static bool visible_return_record_queue_push(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define record_queue_push(...) visible_return_record_queue_push("record_queue_push(" #__VA_ARGS__ ")", (record_queue_push)(__VA_ARGS__))
static bool visible_return_record_queue_pop(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define record_queue_pop(...) visible_return_record_queue_pop("record_queue_pop(" #__VA_ARGS__ ")", (record_queue_pop)(__VA_ARGS__))

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
    unsigned char storage[128]; record_queue_t *q=NULL; assert(record_queue_required_bytes()<=sizeof storage); assert(record_queue_init(storage,sizeof storage,&q)); uint8_t out=0U; assert(record_queue_push(q,42U)); assert(record_queue_pop(q,&out)&&out==42U); assert(!record_queue_pop(q,&out)); assert(!record_queue_init(storage,1U,&q));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
