#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>

struct integration_fake{int32_t value;uint32_t tick;enum logger_io read_result,store_result,send_results[4];size_t send_count,send_index;unsigned store_calls,send_calls;}; static enum logger_io integration_read(void *c,int32_t *out){struct integration_fake *f=c;if(f->read_result==LOGGER_IO_OK)*out=f->value;return f->read_result;} static uint32_t integration_now(void *c){return ((struct integration_fake *)c)->tick;} static enum logger_io integration_store(void *c,const uint8_t *b,size_t n){struct integration_fake *f=c;(void)b;(void)n;++f->store_calls;return f->store_result;} static enum logger_io integration_send(void *c,const uint8_t *b,size_t n){struct integration_fake *f=c;(void)b;(void)n;++f->send_calls;if(f->send_index<f->send_count)return f->send_results[f->send_index++];return LOGGER_IO_OK;}

static enum logger_result visible_return_logger_init(const char *call, enum logger_result value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define logger_init(...) visible_return_logger_init("logger_init(" #__VA_ARGS__ ")", (logger_init)(__VA_ARGS__))
static enum logger_result visible_return_logger_capture(const char *call, enum logger_result value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define logger_capture(...) visible_return_logger_capture("logger_capture(" #__VA_ARGS__ ")", (logger_capture)(__VA_ARGS__))
static enum logger_result visible_return_logger_flush_one(const char *call, enum logger_result value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define logger_flush_one(...) visible_return_logger_flush_one("logger_flush_one(" #__VA_ARGS__ ")", (logger_flush_one)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 7

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
    struct integration_fake f={21000,77U,LOGGER_IO_OK,LOGGER_IO_OK,{LOGGER_IO_TEMPORARY,LOGGER_IO_OK},2U,0U,0U,0U};
struct logger_ports ports={&f,integration_read,integration_now,integration_store,integration_send}; struct integrated_logger logger;
assert(logger_init(&logger,&ports,1U)==LOGGER_OK); assert(logger_capture(&logger)==LOGGER_OK&&logger.count==1U&&logger.next_sequence==1U);
assert(logger_flush_one(&logger)==LOGGER_OK&&logger.count==0U&&f.store_calls==1U&&f.send_calls==2U);
f.value=125001; assert(logger_capture(&logger)==LOGGER_RANGE&&logger.count==0U); f.value=42; f.read_result=LOGGER_IO_TEMPORARY; assert(logger_capture(&logger)==LOGGER_SENSOR_FAILURE);
f.read_result=LOGGER_IO_OK; assert(logger_capture(&logger)==LOGGER_OK); f.store_result=LOGGER_IO_TEMPORARY; assert(logger_flush_one(&logger)==LOGGER_STORAGE_FAILURE&&logger.count==1U);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
