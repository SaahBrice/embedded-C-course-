#ifndef LEARN_LINKER_SCRIPTS_TASK_H
#define LEARN_LINKER_SCRIPTS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool region_contains(uint32_t origin, uint32_t length, uint32_t address, uint32_t size);

#endif
