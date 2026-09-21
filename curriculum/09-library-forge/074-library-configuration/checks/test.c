#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(queue_config_valid(2U,false)); assert(queue_config_valid(128U,true)); assert(!queue_config_valid(0U,false)); assert(!queue_config_valid(3U,false)); assert(!queue_config_valid(2048U,true));
    
    return 0;
}
