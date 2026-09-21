#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>

struct fake_storage{uint8_t bytes[16];size_t length,chunk;bool fail;}; static size_t fake_storage_write(void *c,const uint8_t *b,size_t n){struct fake_storage *s=c;if(s->fail)return 0U;size_t take=n<s->chunk?n:s->chunk;memcpy(s->bytes+s->length,b,take);s->length+=take;return take;}

static bool visible_return_storage_write_all(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define storage_write_all(...) visible_return_storage_write_all("storage_write_all(" #__VA_ARGS__ ")", (storage_write_all)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 2

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
    const uint8_t data[]={1U,2U,3U,4U,5U}; struct fake_storage s={{0U},0U,2U,false}; assert(storage_write_all(fake_storage_write,&s,data,sizeof data)&&s.length==5U&&memcmp(s.bytes,data,5U)==0); s.length=0U;s.fail=true;assert(!storage_write_all(fake_storage_write,&s,data,sizeof data));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
