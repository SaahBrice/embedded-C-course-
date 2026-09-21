/* Mission: Keep Interrupt Work Bounded */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

void interrupt_capture(void *context, uint32_t event) {
    struct interrupt_mailbox *mailbox = context;
    if (mailbox == NULL || mailbox->pending) return;
    mailbox->event = event; mailbox->pending = true;
}
bool interrupt_take(struct interrupt_mailbox *mailbox, uint32_t *out_event) {
    if (mailbox == NULL || out_event == NULL || !mailbox->pending) return false;
    *out_event = mailbox->event; mailbox->pending = false; return true;
}
