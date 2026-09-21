/* Mission: Test Collaborating Modules */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool logger_cycle(const struct logger_ports *ports) {
    if (ports == NULL || ports->read == NULL || ports->store == NULL) return false;
    int32_t value=0;
    return ports->read(ports->context,&value) && ports->store(ports->context,value);
}
