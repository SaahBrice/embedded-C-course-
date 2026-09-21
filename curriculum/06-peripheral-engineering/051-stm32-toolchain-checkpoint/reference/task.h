#ifndef LEARN_STM32_TOOLCHAIN_CHECKPOINT_TASK_H
#define LEARN_STM32_TOOLCHAIN_CHECKPOINT_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool elf_header_targets_arm(const uint8_t *header, size_t length);

#endif
