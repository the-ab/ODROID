# Installation and first login

[Deutsch](INSTALL.de.md)

Download the desired U3 ZIP and its `.sha256` file from the project's [Releases](https://github.com/the-ab/ODROID/releases). A candidate is not a stable release; check the release notes and [hardware status](HARDWARE.md).

```sh
sha256sum -c odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.0.zip.sha256
unzip odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.0.zip
sha256sum -c odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.0.img.sha256
```

Use the matching `minimal` filenames for that variant. Write the **complete IMG** to the chosen SD card or eMMC module through its adapter. This overwrites the target's partition table and installation. On Linux, first identify and unmount its mounted partitions. `/dev/sdX` below is a placeholder for the verified whole target, not a partition:

```sh
lsblk -p -o NAME,SIZE,MODEL,TYPE,MOUNTPOINTS
sudo dd if=odroid-u3-ubuntu-26.04.1-armhf-minimized-v1.0.0.img \
  of=/dev/sdX bs=4M conv=fsync status=progress
sync
```

Disconnect power before moving the module/card. Boot with only the intended boot medium inserted. For a native eMMC module that fails to start but boots through the U3 SD adapter, follow [boot0 recovery](EMMC-RECOVERY.md); repeatedly rewriting the user-area IMG does not update boot0.

Ethernet obtains DHCP. Login is **odroid**, password **odroid**; sudo asks for that password. Root SSH is disabled. New SSH host keys and machine identity are generated on first boot, so a fresh installation legitimately has different SSH host fingerprints. Verify the new device's identity before replacing an old SSH trust entry.

```sh
ssh odroid@HOST
passwd
sudo -v
uname -r
df -h /
systemctl --failed
sudo journalctl -b -p err --no-pager
odroid-fan status
```

The root partition grows on first boot. Defaults are UTC and `en_US.UTF-8`; configure your preferred timezone with `sudo timedatectl set-timezone REGION/CITY`. Power off with `sudo poweroff` or the supported power button, then disconnect supply before moving eMMC hardware.

Ubuntu packages use the normal Ubuntu 26.04 update repositories. The board kernel is supplied by this project and is not an Ubuntu generic kernel package. `minimized` includes the official `unminimize` command to restore stripped content; the `minimal` image additionally installs the Ubuntu minimal/standard metapackages and administration tools listed in `PACKAGES.tsv`.
