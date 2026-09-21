#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>

struct fake_logger{bool read_ok,store_ok;int32_t value,stored;unsigned reads,writes;}; static bool fake_logger_read(void *c,int32_t *out){struct fake_logger *f=c;++f->reads;if(!f->read_ok)return false;*out=f->value;return true;} static bool fake_logger_store(void *c,int32_t v){struct fake_logger *f=c;++f->writes;if(!f->store_ok)return false;f->stored=v;return true;}


int main(void) {
    struct fake_logger f={true,true,42,0,0U,0U}; struct logger_ports p={&f,fake_logger_read,fake_logger_store}; assert(logger_cycle(&p)&&f.stored==42&&f.reads==1U&&f.writes==1U); f.read_ok=false; assert(!logger_cycle(&p)&&f.writes==1U); f.read_ok=true; f.store_ok=false; assert(!logger_cycle(&p));
    
    return 0;
}
