#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(led_output_level(false,true)); assert(!led_output_level(false,false)); assert(!led_output_level(true,true)); assert(led_output_level(true,false));
    
    return 0;
}
