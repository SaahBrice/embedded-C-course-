#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(controller_transition(CONTROLLER_IDLE,EVENT_START)==CONTROLLER_SAMPLING); assert(controller_transition(CONTROLLER_SAMPLING,EVENT_SAMPLE_OK)==CONTROLLER_IDLE); assert(controller_transition(CONTROLLER_SAMPLING,EVENT_SAMPLE_BAD)==CONTROLLER_FAULT); assert(controller_transition(CONTROLLER_FAULT,EVENT_RESET)==CONTROLLER_IDLE); assert(controller_transition((enum controller_state)99,EVENT_RESET)==CONTROLLER_FAULT);
    
    return 0;
}
