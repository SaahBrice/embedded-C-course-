#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint16_t value = 9U; assert(parse_u16("0", &value) && value == 0U); assert(parse_u16("65535", &value) && value == 65535U); assert(!parse_u16("65536", &value)); assert(!parse_u16("-1", &value)); assert(!parse_u16("12x", &value)); assert(!parse_u16("", &value));
    
    return 0;
}
