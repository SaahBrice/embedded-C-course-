SHELL := /bin/sh

CUBE_VERSION := v1.4.1
CUBE_COMMIT := e044287c0582f76d55455426355f133553368d52
LEARN_C_DATA_HOME ?= $(HOME)/.local/share/learn-c
STM32CUBE_C0 ?= $(LEARN_C_DATA_HOME)/STM32CubeC0-v1.4.1
CROSS_COMPILE ?= arm-none-eabi-
CC := $(CROSS_COMPILE)gcc
SIZE := $(CROSS_COMPILE)size

PLATFORM_ROOT := $(abspath ..)
BUILD_DIR := build
ELF := $(BUILD_DIR)/nucleo-c031c6.elf
MAP := $(BUILD_DIR)/nucleo-c031c6.map
LINKER_SCRIPT := stm32c031c6.ld

CMSIS_CORE := $(STM32CUBE_C0)/Drivers/CMSIS/Include
CMSIS_DEVICE := $(STM32CUBE_C0)/Drivers/CMSIS/Device/ST/STM32C0xx
HAL_DRIVER := $(STM32CUBE_C0)/Drivers/STM32C0xx_HAL_Driver

PROJECT_SOURCES := \
	src/main.c \
	src/runtime.c \
	src/stm32c0xx_it.c \
	$(PLATFORM_ROOT)/common/src/app.c \
	$(PLATFORM_ROOT)/target/board_stm32_hal.c \
	$(PLATFORM_ROOT)/target/board_stm32_init.c
VENDOR_SOURCES := \
	$(CMSIS_DEVICE)/Source/Templates/gcc/startup_stm32c031xx.s \
	$(CMSIS_DEVICE)/Source/Templates/system_stm32c0xx.c \
	$(HAL_DRIVER)/Src/stm32c0xx_hal.c \
	$(HAL_DRIVER)/Src/stm32c0xx_hal_cortex.c \
	$(HAL_DRIVER)/Src/stm32c0xx_hal_gpio.c \
	$(HAL_DRIVER)/Src/stm32c0xx_hal_rcc.c \
	$(HAL_DRIVER)/Src/stm32c0xx_hal_uart.c

CPPFLAGS := \
	-DSTM32C031xx -DUSE_HAL_DRIVER \
	-Iinclude \
	-I$(PLATFORM_ROOT)/common/include \
	-I$(PLATFORM_ROOT)/target \
	-I$(CMSIS_CORE) \
	-I$(CMSIS_DEVICE)/Include \
	-I$(HAL_DRIVER)/Inc \
	-I$(HAL_DRIVER)/Inc/Legacy
CFLAGS := \
	-mcpu=cortex-m0plus -mthumb -std=c11 \
	-Wall -Wextra -Wpedantic -Werror \
	-ffunction-sections -fdata-sections -fstack-usage \
	-Os -g3
LDFLAGS := \
	-mcpu=cortex-m0plus -mthumb \
	-nostdlib \
	-T$(LINKER_SCRIPT) \
	-Wl,-Map=$(MAP),--gc-sections \
	-Wl,--print-memory-usage \
	-lgcc

.PHONY: all dependency-check size clean

all: $(ELF) size

dependency-check:
	@if [ ! -d "$(STM32CUBE_C0)" ]; then \
		echo "STM32CubeC0 $(CUBE_VERSION) at commit $(CUBE_COMMIT) is required; this project does not download vendor code." >&2; \
		exit 2; \
	fi
	@if [ ! -f "$(CMSIS_DEVICE)/Source/Templates/gcc/startup_stm32c031xx.s" ] || \
	   [ ! -f "$(HAL_DRIVER)/Src/stm32c0xx_hal.c" ]; then \
		echo "STM32CubeC0 $(CUBE_VERSION) is incomplete at $(STM32CUBE_C0); this project does not download vendor code." >&2; \
		exit 2; \
	fi
	@actual=$$(git -C "$(STM32CUBE_C0)" rev-parse HEAD 2>/dev/null || true); \
	if [ "$$actual" != "$(CUBE_COMMIT)" ]; then \
		echo "STM32CubeC0 must be $(CUBE_VERSION) commit $(CUBE_COMMIT); found '$${actual:-unverifiable}'." >&2; \
		exit 2; \
	fi
	@if ! command -v "$(CC)" >/dev/null 2>&1; then \
		echo "Missing cross compiler: $(CC)" >&2; \
		exit 2; \
	fi

$(ELF): dependency-check $(PROJECT_SOURCES) $(LINKER_SCRIPT) include/stm32c0xx_hal_conf.h
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) $(PROJECT_SOURCES) $(VENDOR_SOURCES) $(LDFLAGS) -o $@

size: $(ELF)
	$(SIZE) $(ELF)

clean:
	rm -rf $(BUILD_DIR)
