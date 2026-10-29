#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-only
set -euo pipefail
kernel=$(realpath -- "${1:?kernel build required}")
output=${2:?new artifact directory required}
[[ ! -e "$output" && -f "$kernel/include/config/kernel.release" ]]
release=$(cat "$kernel/include/config/kernel.release")
[[ $release == 6.12.114-odroidu3-v1 ]]
mkdir -p "$output"
output=$(realpath "$output")
make -C "$kernel" ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH="$output" INSTALL_MOD_STRIP=1 modules_install
depmod -b "$output" "$release"
rm -f "$output/lib/modules/$release/build" "$output/lib/modules/$release/source"
# Normalize merged-/usr module layout for the image assembler.
if [[ -d "$output/lib/modules" && ! -L "$output/lib" ]]; then
    mkdir -p "$output/usr/lib"
    mv "$output/lib/modules" "$output/usr/lib/modules"
    rmdir "$output/lib"
fi
cp "$kernel/arch/arm/boot/zImage" "$output/zImage"
cp "$kernel/arch/arm/boot/dts/samsung/exynos4412-odroidu3.dtb" "$output/exynos4412-odroidu3.dtb"
cp "$kernel/.config" "$output/config"
cp "$kernel/System.map" "$output/System.map"
cp "$kernel/include/config/kernel.release" "$output/kernel.release"
(cd "$output" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$output/../kernel-artifact-checksums.txt"
