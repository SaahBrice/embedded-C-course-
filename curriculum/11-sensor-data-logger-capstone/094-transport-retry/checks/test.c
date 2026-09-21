#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>

struct fake_transport{unsigned temporary_left,calls;enum transport_status final;}; static enum transport_status fake_transport_send(void *c){struct fake_transport *t=c;++t->calls;if(t->temporary_left!=0U){--t->temporary_left;return TRANSPORT_TEMPORARY;}return t->final;}


int main(void) {
    struct fake_transport t={2U,0U,TRANSPORT_OK}; unsigned n=0U; assert(transport_retry(fake_transport_send,&t,4U,&n)==TRANSPORT_OK&&n==3U); t.temporary_left=9U;t.calls=0U;assert(transport_retry(fake_transport_send,&t,2U,&n)==TRANSPORT_TEMPORARY&&n==2U);t.temporary_left=0U;t.final=TRANSPORT_PERMANENT;assert(transport_retry(fake_transport_send,&t,4U,&n)==TRANSPORT_PERMANENT&&n==1U);
    
    return 0;
}
