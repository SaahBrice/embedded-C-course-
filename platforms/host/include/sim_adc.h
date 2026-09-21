#ifndef SIM_ADC_H
#define SIM_ADC_H

#include <stddef.h>
#include <stdint.h>

#define SIM_ADC_CHANNEL_COUNT 8U
#define SIM_ADC_MAX_CODE 4095U

enum sim_adc_result { SIM_ADC_OK = 0, SIM_ADC_ARGUMENT, SIM_ADC_CHANNEL, SIM_ADC_RANGE };

void sim_adc_reset(void);
enum sim_adc_result sim_adc_set(size_t channel, uint16_t code);
enum sim_adc_result sim_adc_read(size_t channel, uint16_t *code);

#endif
