/* Mission: Version an Embedded Library */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

enum version_change classify_version_change(bool breaks_api,bool adds_api){if(breaks_api)return VERSION_MAJOR;if(adds_api)return VERSION_MINOR;return VERSION_PATCH;}
