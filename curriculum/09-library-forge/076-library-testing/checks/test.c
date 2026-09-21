#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(ring_state_valid(0U,0U,0U,4U)); assert(ring_state_valid(0U,0U,4U,4U)); assert(ring_state_valid(3U,1U,2U,4U)); assert(!ring_state_valid(4U,0U,0U,4U)); assert(!ring_state_valid(0U,0U,1U,0U));
    
    return 0;
}
