#!/usr/bin/env bash
set -euo pipefail

data_root=${XDG_DATA_HOME:-"$HOME/.local/share"}/learn-c
toolchain_root=$data_root/arm-none-eabi
cube_root=$data_root/STM32CubeC0-v1.4.1
user_bin=$HOME/.local/bin
cube_commit=e044287c0582f76d55455426355f133553368d52

mkdir -p "$data_root" "$toolchain_root" "$user_bin"

if [ ! -x "$toolchain_root/usr/bin/arm-none-eabi-gcc" ]; then
    download_root=$(mktemp -d /tmp/learn-c-arm-debs.XXXXXX)
    (
        cd "$download_root"
        apt-get download binutils-arm-none-eabi gcc-arm-none-eabi
    )
    for package_file in "$download_root"/*.deb; do
        dpkg-deb -x "$package_file" "$toolchain_root"
    done
fi

for tool_name in arm-none-eabi-gcc arm-none-eabi-size arm-none-eabi-readelf arm-none-eabi-objcopy arm-none-eabi-objdump; do
    source_path=$toolchain_root/usr/bin/$tool_name
    destination_path=$user_bin/$tool_name
    if [ ! -e "$destination_path" ]; then
        ln -s "$source_path" "$destination_path"
    elif [ "$(readlink -f "$destination_path")" != "$source_path" ]; then
        echo "Refusing to replace existing $destination_path" >&2
        exit 2
    fi
done

if [ ! -d "$cube_root/.git" ]; then
    git clone --depth 1 --branch v1.4.1 --recurse-submodules --shallow-submodules \
        https://github.com/STMicroelectronics/STM32CubeC0.git "$cube_root"
fi

actual_commit=$(git -C "$cube_root" rev-parse HEAD)
if [ "$actual_commit" != "$cube_commit" ]; then
    echo "STM32CubeC0 has unexpected commit $actual_commit" >&2
    exit 2
fi

"$toolchain_root/usr/bin/arm-none-eabi-gcc" --version | head -n 1
echo "STM32CubeC0: $actual_commit"
echo "Setup complete. Ensure $user_bin is on PATH, then run:"
echo "  make -C platforms/stm32c031 target-build"
