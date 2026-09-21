#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>

struct fake_hal{int32_t value;bool alarm;bool read_ok;}; static bool fake_read(void *c,int32_t *out){struct fake_hal *f=c;if(!f->read_ok)return false;*out=f->value;return true;} static void fake_alarm(void *c,bool on){((struct fake_hal *)c)->alarm=on;}


int main(void) {
    struct fake_hal fake={42,false,true}; struct controller_hal hal={&fake,fake_read,fake_alarm}; assert(controller_step(&hal,40)&&fake.alarm); fake.value=10; assert(controller_step(&hal,40)&&!fake.alarm); fake.read_ok=false; assert(!controller_step(&hal,40)&&fake.alarm);
    
    return 0;
}
