/* Mission: Implement a Tiny Scheduler */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool scheduler_release(struct scheduled_task *task,uint32_t now){if(task==NULL||task->period==0U||(int32_t)(now-task->next_release)<0)return false;task->next_release+=task->period;++task->runs;return true;}
