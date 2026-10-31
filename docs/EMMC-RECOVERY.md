# ODROID-U3 eMMC boot0 recovery

[Deutsch](EMMC-RECOVERY.de.md)

Use this procedure when the same module boots through the eMMC-to-microSD adapter in the U3's SD slot but does not start from the native eMMC socket. An image written with an ordinary SD/USB reader normally updates only the eMMC **user area**. The U3's native eMMC boot chain is in a separate hardware partition, Linux `mmcblkNboot0`.

Updating boot0 is stored on that module. A subsequent ordinary user-area image write preserves it. The replacement image must still contain compatible U3 boot files. This procedure writes rewritable flash, not SoC fuses.

## Files and supported path

The image ZIP contains the complete IMG, `BUILD-MANIFEST.json`, `u3-boot0-prefix.bin`, this guide and `u3-emmc-boot0.py`. Check the ZIP checksum before extracting it. The prefix must have **1,240,064 bytes**; its exact SHA256 is in `BUILD-MANIFEST.json`.

Run the Python tool **on the U3**, using the eMMC module in the adapter directly in the U3 SD slot. A USB reader exposing `/dev/sdX` generally does not expose the hardware boot partitions. The tool refuses non-U3 boards, SD cards, `/dev/sdX`, mismatched CIDs and firmware writes from the native eMMC boot path. Never use the U3 files on XU4.

The guarded write path currently requires the tested configuration: boot0 selected with boot acknowledgement (`PARTITION_CONFIG & 0xf8 == 0x48`), 4-bit legacy boot bus (`BOOT_BUS_WIDTH == 0x01`), and no boot write protection. It does not change these settings automatically. A different configuration requires separate inspection.

## 1. Boot the module through the SD adapter

1. Write the complete project IMG to the eMMC **user area**, using the adapter and an image writer.
2. With power disconnected, remove any module from the native eMMC socket and insert the test module in its adapter into the U3 SD slot.
3. Boot, log in as `odroid` with password `odroid`, and copy the tool, prefix and manifest to a working directory on the U3.
4. Identify the card and root filesystem:

```sh
findmnt -n -o SOURCE,FSTYPE /
lsblk -p -o NAME,SIZE,TYPE,MOUNTPOINTS
```

For the tested SD-adapter path, root was `/dev/mmcblk2p2` and the **whole card** was `/dev/mmcblk2`. Numbering must be checked on your running system. The following example uses that verified device:

```sh
device=/dev/mmcblk2
sudo python3 u3-emmc-boot0.py inspect --device "$device"
```

Check `root_on_selected_card: true`, `sd_adapter_path: true`, the module name, CID, boot partition size and configuration. The tested 16 GB SDW16G modules have 4 MiB boot0/boot1; the payload replaces only their first 1.24 MB in boot0.

## 2. Make and export this module's backup

```sh
cid=$(cat "/sys/class/block/${device##*/}/device/cid")
backup_dir="$HOME/emmc-backups/$cid-$(date +%Y%m%d-%H%M%S)"
sudo python3 u3-emmc-boot0.py backup \
  --device "$device" --backup "$backup_dir"
```

The tool saves and reads back:

- complete `boot0.bin` and `boot1.bin`;
- the first 16 MiB of the user area, including its partition table and SD boot chain;
- raw read-only EXT_CSD data and `BACKUP.json` with identity, sizes and SHA256 values.

This is a boot backup, not a backup of all OS/user data. Copy the whole backup directory **off the module** before applying firmware. For example, from your PC:

```sh
scp -r odroid@HOST:~/emmc-backups ./
```

Use the CID from this SD-adapter session. Do not borrow a backup or CID from another module or copy a CID reported by a different controller.

## 3. Verify and apply the prefix

From the directory containing the extracted manifest and payload:

```sh
payload_sha256=$(python3 -c 'import json; print(json.load(open("BUILD-MANIFEST.json"))["emmc_boot0_payload"]["sha256"])')
printf '%s  %s\n' "$payload_sha256" u3-boot0-prefix.bin | sha256sum -c -
wc -c u3-boot0-prefix.bin

sudo python3 u3-emmc-boot0.py apply \
  --device "$device" --backup "$backup_dir" \
  --payload u3-boot0-prefix.bin --payload-sha256 "$payload_sha256" \
  --confirm-cid "$cid"
```

This command explicitly authorizes the boot0 firmware write to the identified module. It validates the backup and current state, temporarily changes `force_ro`, exclusively opens boot0, writes only the prefix, performs `fsync`, and compares the **entire** boot0 partition. Its tail, boot1, user-area boot prefix and persistent boot configuration must remain unchanged. An already matching state produces no write.

Caught write/readback failures restore the original prefix. Ordinary interruption signals are deferred until the short write/verification/relock transaction finishes. A power loss or forced process kill cannot be made safe by software. The SD-adapter boot chain in the user area is not written by this operation.

Successful output includes `force_ro: "1"`, `boot1_unchanged: true`, `boot_configuration_unchanged: true`, and the new full boot0 SHA256. An `APPLY-*.json` record is saved in the backup directory. The tool does not reboot.

## 4. Test native eMMC boot

```sh
sudo poweroff
```

Wait for shutdown, disconnect the 5 V supply, remove the SD adapter, and fit the module in the native eMMC socket. Leave the SD slot empty and power up. Check the heartbeat LED, DHCP/SSH login and then:

```sh
findmnt -n -o SOURCE,FSTYPE /
uname -r
systemctl --failed
sudo journalctl -b -p err --no-pager
odroid-fan status
```

Native root was `/dev/mmcblk0p2` on the tested boards. Confirm your actual device instead of relying on this numbering.

## Restore the saved state

If necessary, power down and boot the same module through the SD adapter again. Use its own backup and the full `after_sha256` from the corresponding `APPLY-*.json`:

```sh
sudo python3 u3-emmc-boot0.py restore \
  --device "$device" --backup "$backup_dir" --confirm-cid "$cid" \
  --expect-current-sha256 FULL_AFTER_SHA256_FROM_APPLY_RECORD
```

Restore refuses an unexpected current firmware state or changed tail. It writes only the saved prefix, verifies the complete partition, preserves boot1/configuration and restores read-only protection. A backup made after an earlier repair naturally contains that repaired state; it is not a factory reset. Keep the off-module backup for manual recovery after an interrupted or otherwise unknown state.

## Why the offsets differ

The [upstream U-Boot ODROID guide](https://github.com/u-boot/u-boot/blob/v2026.10/doc/README.odroid) documents these **512-byte sectors**:

| Component | SD/user-area start | eMMC boot0 start | Reserved sectors |
|---|---:|---:|---:|
| BL1 | 1 | 0 | 30 |
| BL2 | 31 | 30 | 29 |
| U-Boot | 63 | 62 | 2048 |
| TrustZone | 2111 | 2110 | 312 |

The prefix covers boot0 sectors 0–2421, including gaps. Do not write a complete IMG to boot0 and do not overwrite a whole 4 MiB boot partition with a shorter prefix. The supplied tool preserves the module-specific tail.

No UART adapter is required for this SD-adapter path. If a serial console is used separately, the U3 UART is **1.8 V**, 115200 8N1.

The prefix has booted two tested 16 GB SDW16G modules after module-specific backups and verified updates. The generic tool has read-only hardware checks and file-based failure/rollback tests; broader module/boot-configuration coverage remains separate from those results. See [hardware status](HARDWARE.md) and [release requirements](RELEASES.md).
