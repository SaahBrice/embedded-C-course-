CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -O0 -g
INCLUDES := -Icommon/include -Ihost
TARGET_TEST_INCLUDES := -Ihost/fake_hal -Icommon/include -Itarget

.PHONY: all host-test target-contract-test target-build clean doctor
all: host-test
host/test_app: common/src/app.c host/board_host.c host/test_app.c
	$(CC) $(CFLAGS) $(INCLUDES) $^ -o $@
host-test: host/test_app
	@status=0; ./host/test_app || status=$$?; rm -f host/test_app; exit $$status
host/test_target_adapter: target/board_stm32_hal.c target/board_stm32_init.c host/test_target_adapter.c
	$(CC) $(CFLAGS) $(TARGET_TEST_INCLUDES) $^ -o $@
target-contract-test: host/test_target_adapter
	@status=0; ./host/test_target_adapter || status=$$?; rm -f host/test_target_adapter; exit $$status
target-build:
	$(MAKE) -C target_project clean all
	arm-none-eabi-readelf -h target_project/build/nucleo-c031c6.elf | grep -E 'Machine:[[:space:]]+ARM'
doctor:
	python3 doctor.py
clean:
	rm -f host/test_app host/test_target_adapter
	$(MAKE) -C target_project clean >/dev/null
