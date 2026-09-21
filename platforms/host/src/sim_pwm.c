#include "sim_pwm.h"

struct pwm_channel { uint32_t period; uint32_t compare; };
static struct pwm_channel channels[SIM_PWM_CHANNEL_COUNT];
static size_t updates;

void sim_pwm_reset(void) {
    for (size_t index = 0U; index < SIM_PWM_CHANNEL_COUNT; ++index) {
        channels[index].period = 0U;
        channels[index].compare = 0U;
    }
    updates = 0U;
}

enum sim_pwm_result sim_pwm_configure(size_t channel, uint32_t period_ticks, uint32_t compare_ticks) {
    if (channel >= SIM_PWM_CHANNEL_COUNT) return SIM_PWM_RANGE;
    if (period_ticks == 0U || compare_ticks > period_ticks) return SIM_PWM_ARGUMENT;
    channels[channel].period = period_ticks;
    channels[channel].compare = compare_ticks;
    ++updates;
    return SIM_PWM_OK;
}

enum sim_pwm_result sim_pwm_observe(size_t channel, uint32_t *period_ticks, uint32_t *compare_ticks) {
    if (period_ticks == NULL || compare_ticks == NULL) return SIM_PWM_ARGUMENT;
    if (channel >= SIM_PWM_CHANNEL_COUNT) return SIM_PWM_RANGE;
    *period_ticks = channels[channel].period;
    *compare_ticks = channels[channel].compare;
    return SIM_PWM_OK;
}

size_t sim_pwm_update_count(void) { return updates; }
