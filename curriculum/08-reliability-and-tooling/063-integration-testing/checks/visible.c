#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>

struct fake_logger{bool read_ok,store_ok;int32_t value,stored;unsigned reads,writes;}; static bool fake_logger_read(void *c,int32_t *out){struct fake_logger *f=c;++f->reads;if(!f->read_ok)return false;*out=f->value;return true;} static bool fake_logger_store(void *c,int32_t v){struct fake_logger *f=c;++f->writes;if(!f->store_ok)return false;f->stored=v;return true;}

static bool visible_return_logger_cycle(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define logger_cycle(...) visible_return_logger_cycle("logger_cycle(" #__VA_ARGS__ ")", (logger_cycle)(__VA_ARGS__))

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
    struct fake_logger f={true,true,42,0,0U,0U}; struct logger_ports p={&f,fake_logger_read,fake_logger_store}; assert(logger_cycle(&p)&&f.stored==42&&f.reads==1U&&f.writes==1U); f.read_ok=false; assert(!logger_cycle(&p)&&f.writes==1U); f.read_ok=true; f.store_ok=false; assert(!logger_cycle(&p));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
