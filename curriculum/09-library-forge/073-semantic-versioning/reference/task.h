#ifndef LEARN_SEMANTIC_VERSIONING_TASK_H
#define LEARN_SEMANTIC_VERSIONING_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum version_change { VERSION_PATCH, VERSION_MINOR, VERSION_MAJOR };
enum version_change classify_version_change(bool breaks_api, bool adds_api);

#endif
