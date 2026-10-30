# U3-Kandidaten bauen

[English](BUILD.md)

Benötigt werden ein Linux-Bauhost mit Python ab 3.11, Root-Rechten für die isolierte Chroot, funktionierendem ARM-hard-float-binfmt/QEMU und Platz für Kernel, Rootfs und Image-Zwischendateien. Geprüfter Crosscompiler: GCC 13.3.0. Ubuntu-Beispiel:

```sh
sudo apt install build-essential python3 gnupg patch util-linux xz-utils gcc-arm-linux-gnueabihf binutils-arm-linux-gnueabihf \
  bc bison flex libssl-dev libgnutls28-dev device-tree-compiler u-boot-tools \
  qemu-user-static binfmt-support mtools dosfstools e2fsprogs kmod acl unzip zip shellcheck
```

Im Repository starten und ein **neues** Arbeitsverzeichnis außerhalb von Git verwenden. Bestehende Ausgabeverzeichnisse werden abgewiesen. Der Marker begrenzt Rootfs-Operationen auf ausdrücklich angelegte Image-Wurzeln.

```sh
repo=$(pwd)
work=$(realpath -m ../ODROID-build-v1)
mkdir -p "$work/cache"
touch "$work/.odroid-workspace"
python3 scripts/fetch-sources.py --cache "$work/cache" \
  --boot-reference /pfad/zu/odroid_u3-armv7l-ubuntu20.04minimal-1601403301.zip
```

Auch das passende bereits entpackte Referenz-IMG wird angenommen. Davon werden ausschließlich hashgeprüfte BL1-/BL2-/TrustZone-Blöcke gelesen, niemals Betriebssystem, Benutzer oder Schlüssel. Bootblobs liegen nicht in Git; Weitergabebedingungen bleiben eine Releaseanforderung. Alle Upstream-/Base-/Firmwareeingänge stehen mit Prüfsummen in `sources.lock.json`. Das Ubuntu-Base-Archiv wurde gegen das signierte Manifest mit Ubuntu-CD-Image-Schlüssel `843938DF228D22F7B3742BC0D94AA3F0EFE21092` geprüft.

```sh
bash scripts/build-kernel.sh "$work/cache/linux-6.12.114.tar.xz" "$work/linux-v1"
sudo bash scripts/prepare-kernel-artifacts.sh "$work/linux-v1" "$work/kernel-v1"

mkdir "$work/u-boot"
tar -xzf "$work/cache/u-boot-v2026.10.tar.gz" --strip-components=1 -C "$work/u-boot"
make -C "$work/u-boot" ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- odroid_defconfig
make -C "$work/u-boot" ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -j4
```

U-Boot muss in den reservierten Bereich von 1 MiB passen. Bauzeit und Compiler können den Hash ändern. Tatsächliche Binärdatei sowie passende Quellen/Konfiguration aufbewahren. Gleicher Quelltag bestätigt keinen realen Start eines neu gebauten Bootloaders.

Für jede Variante `variant=minimized` bzw. `variant=minimal` verwenden:

```sh
variant=minimized
root="$work/rootfs-$variant"
out="$work/output-$variant"
sudo mkdir "$root"
sudo tar --numeric-owner -xpf "$work/cache/ubuntu-base-26.04.1-base-armhf.tar.gz" -C "$root"
sudo unshare --mount --pid --fork bash "$repo/scripts/prepare-rootfs.sh" "$root" "$variant"
sudo unshare --mount --pid --fork bash "$repo/scripts/install-kernel-packages.sh" "$root" "$work/kernel-debs"
sudo python3 "$repo/scripts/assemble-image.py" --root "$root" \
  --kernel "$work/kernel-v1" --uboot "$work/u-boot/u-boot-dtb.bin" \
  --firmware "$work/cache" --output "$out" --variant "$variant"
sudo unshare --mount --pid --fork bash "$repo/scripts/validate-rootfs.sh" "$root" "$variant" \
  > "$work/qa-$variant.log" 2>&1
sudo python3 "$repo/scripts/verify-image.py" --output "$out" --qa-log "$work/qa-$variant.log"
sudo python3 "$repo/scripts/package-image.py" --output "$out"
```

Zusammengebaut werden ausschließlich reguläre Dateien. Das 2-GiB-IMG enthält ab Sektor 32768 eine 256-MiB-FAT16-Bootpartition und eine ext4-Rootpartition, die beim Erststart wächst. Diese Konfiguration benötigt keine initrd. Host-ACLs werden aus Image-Wurzeln entfernt; Dateifähigkeiten und erforderliche Unix-Rechte bleiben erhalten.

APT verwendet aktuelle signierte Ubuntu-26.04-Quellen. `PACKAGES.tsv` hält die tatsächlich installierten Versionen fest. Eingänge und Bauweg sind festgelegt; identische Binärbytes bei später veränderten Paketquellen/Bauumgebungen werden nicht behauptet.

Quellprüfungen: `python3 -m unittest discover -s tests -v`, Python-Kompilierung und shellcheck. Offline-ARM-, Image- und ZIP-Prüfungen ersetzen keinen realen Erststart. Siehe [Releaseanforderungen](RELEASES.de.md).

Das lokale Verzeichnis `kernel-debs` vor dem Imagebau gemäß [Kernelupdates](KERNEL-UPDATES.de.md) erzeugen.
