#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(logger_ports_ready(true,true,true,true)); assert(!logger_ports_ready(false,true,true,true)); assert(!logger_ports_ready(true,false,true,true)); assert(!logger_ports_ready(true,true,false,true)); assert(!logger_ports_ready(true,true,true,false));
    
    return 0;
}
