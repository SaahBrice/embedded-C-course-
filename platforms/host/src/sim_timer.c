#include "sim_timer.h"

#include <stdint.h>

static uint32_t current_tick;

void sim_timer_reset(uint32_t initial_tick) { current_tick = initial_tick; }
void sim_timer_advance(uint32_t ticks) { current_tick += ticks; }
uint32_t sim_timer_now(void) { return current_tick; }
uint32_t sim_timer_elapsed(uint32_t since) { return current_tick - since; }
int sim_timer_deadline_reached(uint32_t deadline) { return (int32_t)(current_tick - deadline) >= 0; }
