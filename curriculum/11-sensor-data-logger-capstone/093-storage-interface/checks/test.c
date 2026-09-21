#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>

struct fake_storage{uint8_t bytes[16];size_t length,chunk;bool fail;}; static size_t fake_storage_write(void *c,const uint8_t *b,size_t n){struct fake_storage *s=c;if(s->fail)return 0U;size_t take=n<s->chunk?n:s->chunk;memcpy(s->bytes+s->length,b,take);s->length+=take;return take;}


int main(void) {
    const uint8_t data[]={1U,2U,3U,4U,5U}; struct fake_storage s={{0U},0U,2U,false}; assert(storage_write_all(fake_storage_write,&s,data,sizeof data)&&s.length==5U&&memcmp(s.bytes,data,5U)==0); s.length=0U;s.fail=true;assert(!storage_write_all(fake_storage_write,&s,data,sizeof data));
    
    return 0;
}
