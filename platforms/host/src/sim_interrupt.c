#include "sim_interrupt.h"

struct interrupt_line { sim_interrupt_handler handler; void *context; bool enabled; };
static struct interrupt_line lines[SIM_INTERRUPT_LINE_COUNT];
static size_t dispatches;

void sim_interrupt_reset(void) {
    for (size_t index = 0U; index < SIM_INTERRUPT_LINE_COUNT; ++index) {
        lines[index].handler = NULL;
        lines[index].context = NULL;
        lines[index].enabled = false;
    }
    dispatches = 0U;
}

enum sim_interrupt_result sim_interrupt_register(size_t line, sim_interrupt_handler handler, void *context) {
    if (line >= SIM_INTERRUPT_LINE_COUNT) return SIM_INTERRUPT_RANGE;
    if (handler == NULL) return SIM_INTERRUPT_ARGUMENT;
    lines[line].handler = handler;
    lines[line].context = context;
    return SIM_INTERRUPT_OK;
}

enum sim_interrupt_result sim_interrupt_enable(size_t line, bool enabled) {
    if (line >= SIM_INTERRUPT_LINE_COUNT) return SIM_INTERRUPT_RANGE;
    lines[line].enabled = enabled;
    return SIM_INTERRUPT_OK;
}

enum sim_interrupt_result sim_interrupt_trigger(size_t line, uint32_t event) {
    if (line >= SIM_INTERRUPT_LINE_COUNT) return SIM_INTERRUPT_RANGE;
    if (!lines[line].enabled) return SIM_INTERRUPT_DISABLED;
    if (lines[line].handler == NULL) return SIM_INTERRUPT_ARGUMENT;
    lines[line].handler(lines[line].context, event);
    ++dispatches;
    return SIM_INTERRUPT_OK;
}

size_t sim_interrupt_dispatch_count(void) { return dispatches; }
