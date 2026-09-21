#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>

struct fake_sensor{enum sensor_status status;int32_t value;}; static enum sensor_status fake_sensor_read(void *c,int32_t *out){struct fake_sensor *f=c;if(f->status==SENSOR_OK)*out=f->value;return f->status;}

static enum sensor_status visible_return_sensor_read_checked(const char *call, enum sensor_status value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define sensor_read_checked(...) visible_return_sensor_read_checked("sensor_read_checked(" #__VA_ARGS__ ")", (sensor_read_checked)(__VA_ARGS__))

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
    struct fake_sensor f={SENSOR_OK,25}; int32_t out=0; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_OK&&out==25); f.value=101; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_RANGE); f.status=SENSOR_UNAVAILABLE; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_UNAVAILABLE);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
