#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>

struct fake_transport{unsigned temporary_left,calls;enum transport_status final;}; static enum transport_status fake_transport_send(void *c){struct fake_transport *t=c;++t->calls;if(t->temporary_left!=0U){--t->temporary_left;return TRANSPORT_TEMPORARY;}return t->final;}

static enum transport_status visible_return_transport_retry(const char *call, enum transport_status value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define transport_retry(...) visible_return_transport_retry("transport_retry(" #__VA_ARGS__ ")", (transport_retry)(__VA_ARGS__))

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
    struct fake_transport t={2U,0U,TRANSPORT_OK}; unsigned n=0U; assert(transport_retry(fake_transport_send,&t,4U,&n)==TRANSPORT_OK&&n==3U); t.temporary_left=9U;t.calls=0U;assert(transport_retry(fake_transport_send,&t,2U,&n)==TRANSPORT_TEMPORARY&&n==2U);t.temporary_left=0U;t.final=TRANSPORT_PERMANENT;assert(transport_retry(fake_transport_send,&t,4U,&n)==TRANSPORT_PERMANENT&&n==1U);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
