#ifndef SIM_TIMER_H
#define SIM_TIMER_H

#include <stdint.h>

void sim_timer_reset(uint32_t initial_tick);
void sim_timer_advance(uint32_t ticks);
uint32_t sim_timer_now(void);
uint32_t sim_timer_elapsed(uint32_t since);
int sim_timer_deadline_reached(uint32_t deadline);

#endif
