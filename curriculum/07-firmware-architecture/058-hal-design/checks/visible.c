#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>

struct fake_hal{int32_t value;bool alarm;bool read_ok;}; static bool fake_read(void *c,int32_t *out){struct fake_hal *f=c;if(!f->read_ok)return false;*out=f->value;return true;} static void fake_alarm(void *c,bool on){((struct fake_hal *)c)->alarm=on;}

static bool visible_return_controller_step(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define controller_step(...) visible_return_controller_step("controller_step(" #__VA_ARGS__ ")", (controller_step)(__VA_ARGS__))

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
    struct fake_hal fake={42,false,true}; struct controller_hal hal={&fake,fake_read,fake_alarm}; assert(controller_step(&hal,40)&&fake.alarm); fake.value=10; assert(controller_step(&hal,40)&&!fake.alarm); fake.read_ok=false; assert(!controller_step(&hal,40)&&fake.alarm);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
