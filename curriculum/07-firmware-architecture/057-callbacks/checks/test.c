#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>

static bool capture_status(void *context,uint8_t value){*(unsigned *)context += value;return true;}


int main(void) {
    unsigned total=1U; assert(callback_run_once(capture_status,&total,4U)&&total==5U); assert(!callback_run_once(NULL,&total,3U)&&total==5U);
    
    return 0;
}
