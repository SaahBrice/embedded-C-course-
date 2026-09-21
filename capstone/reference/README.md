# Portable Sensor Data Logger

This is the completed reference product for the final campaign. It is allocation-free and separates the portable logger core from sensor, clock, storage, and transport adapters.

The logger validates complete samples before mutation, rejects new records when its fixed queue is full, injects monotonic timestamps, serializes a versioned little-endian wire format, preserves records across storage/transport failures, avoids duplicate storage after a successful persist, and uses bounded transport retries.

Run `make test`, then `./logger_demo`. A second supported build is `cmake -S . -B build && cmake --build build && ctest --test-dir build`.

An STM32 adapter supplies the four port callbacks using ADC or I2C sensors, `HAL_GetTick`, flash/EEPROM/SD storage, and USART/SPI transport. The portable core itself contains no STM32 headers.
