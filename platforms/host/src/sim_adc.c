#include "sim_adc.h"

static uint16_t channels[SIM_ADC_CHANNEL_COUNT];

void sim_adc_reset(void) {
    for (size_t index = 0U; index < SIM_ADC_CHANNEL_COUNT; ++index) channels[index] = 0U;
}

enum sim_adc_result sim_adc_set(size_t channel, uint16_t code) {
    if (channel >= SIM_ADC_CHANNEL_COUNT) return SIM_ADC_CHANNEL;
    if (code > SIM_ADC_MAX_CODE) return SIM_ADC_RANGE;
    channels[channel] = code;
    return SIM_ADC_OK;
}

enum sim_adc_result sim_adc_read(size_t channel, uint16_t *code) {
    if (code == NULL) return SIM_ADC_ARGUMENT;
    if (channel >= SIM_ADC_CHANNEL_COUNT) return SIM_ADC_CHANNEL;
    *code = channels[channel];
    return SIM_ADC_OK;
}
