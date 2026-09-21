#ifndef LEARN_INTERRUPTS_TASK_H
#define LEARN_INTERRUPTS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

struct interrupt_mailbox { uint32_t event; bool pending; };
void interrupt_capture(void *context, uint32_t event);
bool interrupt_take(struct interrupt_mailbox *mailbox, uint32_t *out_event);

#endif
