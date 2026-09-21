#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>

static bool capture_handler(void *context,uint8_t value){*(unsigned *)context += value;return true;}


int main(void) {
    event_handler handlers[] = {capture_handler, NULL}; unsigned total = 0U;
assert(event_dispatch(0U,handlers,2U,&total,7U) && total == 7U); assert(!event_dispatch(1U,handlers,2U,&total,1U)); assert(!event_dispatch(2U,handlers,2U,&total,1U));
    
    return 0;
}
