/* Mission: Capstone: Partition the System */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool logger_ports_ready(bool sensor,bool clock,bool storage,bool transport){return sensor&&clock&&storage&&transport;}
