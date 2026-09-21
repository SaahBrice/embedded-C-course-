/* Mission: Capstone: Buffer Records */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool record_ring_push(struct record_ring *r,struct log_record v){if(r==NULL||r->count==RECORD_RING_CAPACITY)return false;r->data[r->head]=v;r->head=(r->head+1U)%RECORD_RING_CAPACITY;++r->count;return true;} bool record_ring_pop(struct record_ring *r,struct log_record *out){if(r==NULL||out==NULL||r->count==0U)return false;*out=r->data[r->tail];r->tail=(r->tail+1U)%RECORD_RING_CAPACITY;--r->count;return true;}
