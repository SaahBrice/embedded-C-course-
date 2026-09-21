#include "sim_mmio.h"

static uint32_t registers[SIM_MMIO_REGISTER_COUNT];
static size_t reads;
static size_t writes;

void sim_mmio_reset(void) {
    for (size_t index = 0U; index < SIM_MMIO_REGISTER_COUNT; ++index) registers[index] = 0U;
    reads = 0U;
    writes = 0U;
}

enum sim_mmio_result sim_mmio_read(size_t index, uint32_t *value) {
    if (value == NULL) return SIM_MMIO_ARGUMENT;
    if (index >= SIM_MMIO_REGISTER_COUNT) return SIM_MMIO_RANGE;
    *value = registers[index];
    ++reads;
    return SIM_MMIO_OK;
}

enum sim_mmio_result sim_mmio_write(size_t index, uint32_t value) {
    if (index >= SIM_MMIO_REGISTER_COUNT) return SIM_MMIO_RANGE;
    registers[index] = value;
    ++writes;
    return SIM_MMIO_OK;
}

enum sim_mmio_result sim_mmio_update(size_t index, uint32_t clear_mask, uint32_t set_mask) {
    if (index >= SIM_MMIO_REGISTER_COUNT) return SIM_MMIO_RANGE;
    registers[index] = (registers[index] & ~clear_mask) | set_mask;
    ++reads;
    ++writes;
    return SIM_MMIO_OK;
}

size_t sim_mmio_read_count(void) { return reads; }
size_t sim_mmio_write_count(void) { return writes; }
