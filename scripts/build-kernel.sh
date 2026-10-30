#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-only
set -euo pipefail
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
archive=$(realpath -- "${1:?linux archive required}")
build=${2:?new build directory required}
release=${3:-6.12.114-odroidu3-v1}
[[ $release =~ ^6\.12\.114-odroidu3-v[0-9]+$ ]]
[[ ! -e "$build" ]]
printf '%s  %s\n' 7a8589912bd7a8adb07fed074283652cf482a35facef8954554654f0154b4af3 "$archive" | sha256sum -c -
mkdir -p -- "$build"
tar -xJf "$archive" --strip-components=1 --no-same-owner -C "$build"
patch -d "$build" -p1 --dry-run -i "$repo/boards/u3/patches/platform.patch"
patch -d "$build" -p1 -i "$repo/boards/u3/patches/platform.patch"
cp "$repo/boards/u3/kernel.config" "$build/.config"
"$build/scripts/config" --file "$build/.config" --set-str LOCALVERSION "${release#6.12.114}" --disable LOCALVERSION_AUTO
export ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-
export KBUILD_BUILD_USER=builder KBUILD_BUILD_HOST=odroid KBUILD_BUILD_VERSION=1
export SOURCE_DATE_EPOCH=1793307600 KBUILD_BUILD_TIMESTAMP='Thu Oct 29 21:00:00 UTC 2026'
make -C "$build" olddefconfig
make -C "$build" -j"${JOBS:-4}" zImage modules dtbs
test "$(cat "$build/include/config/kernel.release")" = "$release"
