# Repository-owned STM32C031C6 target

This project compiles and links the portable application for Cortex-M0+ using
repository-owned board initialization and linker configuration. It uses the
official STM32CubeC0 v1.4.1 source at one verified commit.

From the repository root:

The one-time `./scripts/setup_arm_toolchain.sh` command installs ARM GCC and the
pinned Cube checkout below your user data directory; it does not need `sudo`.
After that, build and identify the actual ARM ELF with:

```sh
make -C platforms/stm32c031 target-build
```

If you already manage these dependencies elsewhere, override `STM32CUBE_C0`
and `CROSS_COMPILE` on the Make command line.

`STM32CUBE_C0` must be a Git checkout at commit
`e044287c0582f76d55455426355f133553368d52` (tag `v1.4.1`). The build guard
fails instead of downloading or silently selecting another vendor revision.
Outputs are `build/nucleo-c031c6.elf` and `build/nucleo-c031c6.map`; `make clean`
removes the complete build directory.
