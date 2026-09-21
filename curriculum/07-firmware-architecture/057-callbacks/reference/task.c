/* Mission: Inject Behavior with Callbacks */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool callback_run_once(status_callback callback,void *context,uint8_t value){return callback!=NULL&&callback(context,value);}
