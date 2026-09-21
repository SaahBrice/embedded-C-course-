#ifndef LEARN_MEMORY_SECTIONS_TASK_H
#define LEARN_MEMORY_SECTIONS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum object_section { SECTION_RODATA, SECTION_DATA, SECTION_BSS, SECTION_NOINIT };
enum object_section choose_object_section(bool writable, bool has_nonzero_initializer, bool retain_across_reset);

#endif
