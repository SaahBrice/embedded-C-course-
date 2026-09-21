#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(logger_requirements_valid(1000U,100U,64U)); assert(!logger_requirements_valid(0U,0U,64U)); assert(!logger_requirements_valid(1000U,101U,64U)); assert(!logger_requirements_valid(1000U,50U,1U));
    
    return 0;
}
