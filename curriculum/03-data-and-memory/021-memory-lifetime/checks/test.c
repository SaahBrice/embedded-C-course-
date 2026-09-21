#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    int16_t source=-7,destination=4; assert(snapshot_i16(&source,&destination)&&destination==-7); source=12; assert(destination==-7); assert(!snapshot_i16(NULL,&destination)); assert(!snapshot_i16(&source,NULL));
    
    return 0;
}
