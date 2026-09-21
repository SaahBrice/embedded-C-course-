#ifndef LEARN_TRANSPORT_RETRY_TASK_H
#define LEARN_TRANSPORT_RETRY_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum transport_status { TRANSPORT_OK, TRANSPORT_TEMPORARY, TRANSPORT_PERMANENT };
typedef enum transport_status (*transport_send_fn)(void *context);
enum transport_status transport_retry(transport_send_fn send, void *context, unsigned max_attempts, unsigned *out_attempts);

#endif
