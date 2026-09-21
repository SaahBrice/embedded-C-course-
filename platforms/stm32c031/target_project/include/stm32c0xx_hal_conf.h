#ifndef STM32C0XX_HAL_CONF_H
#define STM32C0XX_HAL_CONF_H

#define HAL_MODULE_ENABLED
#define HAL_CORTEX_MODULE_ENABLED
#define HAL_FLASH_MODULE_ENABLED
#define HAL_GPIO_MODULE_ENABLED
#define HAL_PWR_MODULE_ENABLED
#define HAL_RCC_MODULE_ENABLED
#define HAL_UART_MODULE_ENABLED

#define USE_HAL_UART_REGISTER_CALLBACKS 0U

#ifndef HSE_VALUE
#define HSE_VALUE 8000000UL
#endif
#ifndef HSE_STARTUP_TIMEOUT
#define HSE_STARTUP_TIMEOUT 100UL
#endif
#ifndef HSI_VALUE
#define HSI_VALUE 48000000UL
#endif
#ifndef LSI_VALUE
#define LSI_VALUE 32000UL
#endif
#ifndef LSI_STARTUP_TIME
#define LSI_STARTUP_TIME 130UL
#endif
#ifndef LSE_VALUE
#define LSE_VALUE 32768UL
#endif
#ifndef LSE_STARTUP_TIMEOUT
#define LSE_STARTUP_TIMEOUT 5000UL
#endif

#define VDD_VALUE 3300UL
#define TICK_INT_PRIORITY 3U
#define USE_RTOS 0U
#define PREFETCH_ENABLE 0U
#define INSTRUCTION_CACHE_ENABLE 1U

#include "stm32c0xx_hal_rcc.h"
#include "stm32c0xx_hal_gpio.h"
#include "stm32c0xx_hal_cortex.h"
#include "stm32c0xx_hal_flash.h"
#include "stm32c0xx_hal_pwr.h"
#include "stm32c0xx_hal_uart.h"

#define assert_param(expression) ((void)0U)

#endif
