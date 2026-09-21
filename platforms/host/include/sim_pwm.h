#ifndef SIM_PWM_H
#define SIM_PWM_H

#include <stddef.h>
#include <stdint.h>

#define SIM_PWM_CHANNEL_COUNT 4U

enum sim_pwm_result { SIM_PWM_OK = 0, SIM_PWM_ARGUMENT, SIM_PWM_RANGE };

void sim_pwm_reset(void);
enum sim_pwm_result sim_pwm_configure(size_t channel, uint32_t period_ticks, uint32_t compare_ticks);
enum sim_pwm_result sim_pwm_observe(size_t channel, uint32_t *period_ticks, uint32_t *compare_ticks);
size_t sim_pwm_update_count(void);

#endif
