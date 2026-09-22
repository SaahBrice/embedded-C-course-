#include "task.h"
#include <limits.h>


bool instance_increment(unsigned *state){
    if (state==NULL || *state == UINT_MAX) return false;
    (*state)++;
    return true;
    
}


/* TODO — Reason About Scope and Storage: implement the declared interface.
 * Contract to prove: Caller-owned state keeps independent instances separate and refuses unsigned wraparound.
 */
