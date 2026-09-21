#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(controller_config_valid(1000U,-40,125)); assert(!controller_config_valid(0U,-40,125)); assert(!controller_config_valid(60001U,-40,125)); assert(!controller_config_valid(10U,5,4));
    
    return 0;
}
