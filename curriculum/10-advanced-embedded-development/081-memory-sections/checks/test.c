#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(choose_object_section(false,true,false)==SECTION_RODATA); assert(choose_object_section(true,true,false)==SECTION_DATA); assert(choose_object_section(true,false,false)==SECTION_BSS); assert(choose_object_section(true,false,true)==SECTION_NOINIT);
    
    return 0;
}
