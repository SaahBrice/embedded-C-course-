/* Mission: Build a Library Test Matrix */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool ring_state_valid(size_t head,size_t tail,size_t count,size_t capacity){return capacity!=0U&&head<capacity&&tail<capacity&&count<=capacity;}
