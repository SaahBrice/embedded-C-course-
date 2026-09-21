#ifndef LEARN_PWM_TASK_H
#define LEARN_PWM_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool pwm_compare(uint32_t period_ticks, uint8_t duty_percent, uint32_t *out_compare);

#endif
