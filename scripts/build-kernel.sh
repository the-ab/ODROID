#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-only
set -euo pipefail
repo=$(cd -- "$(dirname -- "$0")/.." && pwd)
archive=$(realpath -- "${1:?linux archive required}")
build=${2:?new build directory required}
default_release=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["kernel_release"])' "$repo/boards/u3/board.json")
release=${3:-$default_release}
profile=${4:-}
config="$repo/boards/u3/kernel.config"
patchfile="$repo/boards/u3/patches/platform.patch"
build_epoch=1793362237
require_server=1
archive_hash=fa595aad93734f829c963c2a90ef7c3673224fd7fdae7b49406e397cde2de231
if [[ -n $profile ]]; then
    profile=$(realpath -- "$profile")
    read -r archive_hash expected_release build_epoch require_server < <(python3 - "$profile/source.json" <<'JSON'
import json,sys
p=json.load(open(sys.argv[1]));print(p['sha256'],p['kernel_release'],p.get('source_date_epoch',1793307600),int(p.get('server_profile',False)))
JSON
    )
    [[ $release == "$expected_release" ]]
    config="$profile/kernel.config"
    patchfile="$profile/platform.patch"
else
    [[ $release == "$default_release" ]]
fi
[[ $release =~ ^[0-9]+\.[0-9]+\.[0-9]+-odroidu3-v[0-9]+$ ]]
[[ ! -e "$build" ]]
printf '%s  %s\n' "$archive_hash" "$archive" | sha256sum -c -
mkdir -p -- "$build"
tar -xJf "$archive" --strip-components=1 --no-same-owner -C "$build"
patch -d "$build" -p1 --dry-run -i "$patchfile"
patch -d "$build" -p1 -i "$patchfile"
cp "$config" "$build/.config"
"$build/scripts/config" --file "$build/.config" --set-str LOCALVERSION "-${release#*-}" --disable LOCALVERSION_AUTO
export ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-
export KBUILD_BUILD_USER=builder KBUILD_BUILD_HOST=odroid KBUILD_BUILD_VERSION=1
export SOURCE_DATE_EPOCH=$build_epoch
KBUILD_BUILD_TIMESTAMP=${KBUILD_BUILD_TIMESTAMP:-$(date -u -d "@$build_epoch" "+%a %b %d %H:%M:%S UTC %Y")}
export KBUILD_BUILD_TIMESTAMP
make -C "$build" olddefconfig
if [[ $require_server == 1 ]]; then
    python3 "$repo/scripts/check-server-config.py" --config "$build/.config"
fi
make -C "$build" -j"${JOBS:-4}" zImage modules dtbs
test "$(cat "$build/include/config/kernel.release")" = "$release"
