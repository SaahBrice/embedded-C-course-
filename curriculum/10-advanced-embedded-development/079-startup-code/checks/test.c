#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint32_t words[]={1U,2U,3U}; assert(zero_bss_words(words,3U)&&words[0]==0U&&words[2]==0U); assert(zero_bss_words(NULL,0U)); assert(!zero_bss_words(NULL,1U));
    
    return 0;
}
