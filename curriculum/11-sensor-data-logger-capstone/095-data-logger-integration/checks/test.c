#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>

struct integration_fake{int32_t value;uint32_t tick;enum logger_io read_result,store_result,send_results[4];size_t send_count,send_index;unsigned store_calls,send_calls;}; static enum logger_io integration_read(void *c,int32_t *out){struct integration_fake *f=c;if(f->read_result==LOGGER_IO_OK)*out=f->value;return f->read_result;} static uint32_t integration_now(void *c){return ((struct integration_fake *)c)->tick;} static enum logger_io integration_store(void *c,const uint8_t *b,size_t n){struct integration_fake *f=c;(void)b;(void)n;++f->store_calls;return f->store_result;} static enum logger_io integration_send(void *c,const uint8_t *b,size_t n){struct integration_fake *f=c;(void)b;(void)n;++f->send_calls;if(f->send_index<f->send_count)return f->send_results[f->send_index++];return LOGGER_IO_OK;}


int main(void) {
    struct integration_fake f={21000,77U,LOGGER_IO_OK,LOGGER_IO_OK,{LOGGER_IO_TEMPORARY,LOGGER_IO_OK},2U,0U,0U,0U};
struct logger_ports ports={&f,integration_read,integration_now,integration_store,integration_send}; struct integrated_logger logger;
assert(logger_init(&logger,&ports,1U)==LOGGER_OK); assert(logger_capture(&logger)==LOGGER_OK&&logger.count==1U&&logger.next_sequence==1U);
assert(logger_flush_one(&logger)==LOGGER_OK&&logger.count==0U&&f.store_calls==1U&&f.send_calls==2U);
f.value=125001; assert(logger_capture(&logger)==LOGGER_RANGE&&logger.count==0U); f.value=42; f.read_result=LOGGER_IO_TEMPORARY; assert(logger_capture(&logger)==LOGGER_SENSOR_FAILURE);
f.read_result=LOGGER_IO_OK; assert(logger_capture(&logger)==LOGGER_OK); f.store_result=LOGGER_IO_TEMPORARY; assert(logger_flush_one(&logger)==LOGGER_STORAGE_FAILURE&&logger.count==1U);
    
    return 0;
}
