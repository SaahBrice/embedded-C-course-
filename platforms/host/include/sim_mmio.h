#ifndef SIM_MMIO_H
#define SIM_MMIO_H

#include <stddef.h>
#include <stdint.h>

#define SIM_MMIO_REGISTER_COUNT 64U

enum sim_mmio_result { SIM_MMIO_OK = 0, SIM_MMIO_ARGUMENT, SIM_MMIO_RANGE };

void sim_mmio_reset(void);
enum sim_mmio_result sim_mmio_read(size_t index, uint32_t *value);
enum sim_mmio_result sim_mmio_write(size_t index, uint32_t value);
enum sim_mmio_result sim_mmio_update(size_t index, uint32_t clear_mask, uint32_t set_mask);
size_t sim_mmio_read_count(void);
size_t sim_mmio_write_count(void);

#endif
