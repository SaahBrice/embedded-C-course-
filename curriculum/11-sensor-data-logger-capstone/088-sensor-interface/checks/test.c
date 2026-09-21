#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>

struct fake_sensor{enum sensor_status status;int32_t value;}; static enum sensor_status fake_sensor_read(void *c,int32_t *out){struct fake_sensor *f=c;if(f->status==SENSOR_OK)*out=f->value;return f->status;}


int main(void) {
    struct fake_sensor f={SENSOR_OK,25}; int32_t out=0; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_OK&&out==25); f.value=101; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_RANGE); f.status=SENSOR_UNAVAILABLE; assert(sensor_read_checked(fake_sensor_read,&f,0,100,&out)==SENSOR_UNAVAILABLE);
    
    return 0;
}
