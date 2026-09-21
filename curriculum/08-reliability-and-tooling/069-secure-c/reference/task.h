#ifndef LEARN_SECURE_C_TASK_H
#define LEARN_SECURE_C_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool frame_payload_length(const uint8_t *frame, size_t received, size_t *out_length);

#endif
