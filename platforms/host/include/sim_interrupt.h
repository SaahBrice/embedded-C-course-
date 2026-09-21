#ifndef SIM_INTERRUPT_H
#define SIM_INTERRUPT_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define SIM_INTERRUPT_LINE_COUNT 8U

typedef void (*sim_interrupt_handler)(void *context, uint32_t event);
enum sim_interrupt_result { SIM_INTERRUPT_OK = 0, SIM_INTERRUPT_ARGUMENT, SIM_INTERRUPT_RANGE, SIM_INTERRUPT_DISABLED };

void sim_interrupt_reset(void);
enum sim_interrupt_result sim_interrupt_register(size_t line, sim_interrupt_handler handler, void *context);
enum sim_interrupt_result sim_interrupt_enable(size_t line, bool enabled);
enum sim_interrupt_result sim_interrupt_trigger(size_t line, uint32_t event);
size_t sim_interrupt_dispatch_count(void);

#endif
