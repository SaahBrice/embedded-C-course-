#ifndef LEARN_BOOT_FLOW_TASK_H
#define LEARN_BOOT_FLOW_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum boot_phase { BOOT_SAFE_OUTPUTS, BOOT_CLOCKS, BOOT_DRIVERS, BOOT_ENABLE_ACTUATORS, BOOT_READY };
enum boot_phase boot_next(enum boot_phase current, bool step_ok);

#endif
