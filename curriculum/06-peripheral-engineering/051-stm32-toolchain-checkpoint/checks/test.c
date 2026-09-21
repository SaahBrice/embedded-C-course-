#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const uint8_t arm[20]={0x7fU,'E','L','F',0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0U,0x28U,0U}; assert(elf_header_targets_arm(arm,20U)); assert(!elf_header_targets_arm(arm,19U)); uint8_t host[20]={0}; memcpy(host,arm,20U); host[18]=0x3eU; assert(!elf_header_targets_arm(host,20U));
    
    return 0;
}
