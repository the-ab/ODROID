# U3 hardware verification

[Deutsch](HARDWARE.de.md)

Status: 6 November 2026. Kernel `7.3.1-odroidu3-v32`, package `7.3.1-33`, tools `1.0.3`. Source support, kernel qualification and the first boot of a fresh image are separate claims.

| Component | Evidence / limit |
|---|---|
| Native eMMC / startup | The qualified kernel passed ten pure warmstarts and five controlled halt/cold starts with normal arguments. Each boot checked four advancing CPU timers, 351 module hashes, boot/configuration payloads, lockdep, audit, services and journal. Fresh minimal 1.0.3 also passed native-eMMC basic first-boot checks; the owner reported a successful warmstart. |
| Fresh image variants | Both variants passed offline ARM/rootfs, filesystem, full partition/boot readback and ZIP roundtrip checks. Fresh minimized and SD first boots remain unverified. Earlier prototype SD boots do not establish acceptance of these files. |
| Server functions | Docker, WireGuard, OpenVPN/TUN, IPv4/IPv6 firewall, Samba/CIFS, NFS4.2, SSHFS, security interfaces, modules, bounded load, ordinary unprivileged io_uring and 16 MiB Ethernet transfer each way passed. See [server scope](SERVER-KERNEL.md). |
| Ethernet / time | DHCP, stable hardware-derived fallback MAC and NTP passed. A permanent driver-provided address takes precedence. No fixed personal MAC is shipped. |
| Fan / thermals / power key | Four fan states exercised, adjustable dedicated 35/45/55 °C trips, CPU protection retained. Clean power-button shutdown was observed on earlier images. See [fan control](FAN.md). |
| Pin controller | Consumed wakeup-IRQ device-link correction verified; the preceding link error did not recur. |
| Audio | Current internal stereo codec loop passed. Headphone playback was physically accepted on earlier kernels. Current microphone input is not accepted. See [audio](AUDIO.md). |
| Mali / HDMI / X11 / Wayland | Earlier connected 1080p60 Xorg/Weston and shader tests passed, including human visual checks. Current v32 physical output and a complete desktop are not newly accepted. See [graphics](GRAPHICS.md). |
| USB / GPIO / I²C / SPI / RTC | Drivers enabled; only exercised paths are accepted. USB host reset during restart is expected; an external device's supply voltage interruption was not measured. |
| Samsung MFC | Driver and licensed firmware included; hardware video decoding not accepted. |
| XU4 | Planned; no U3 boot offsets or acceptance apply to XU4. |

Fresh minimal 1.0.3 matched the complete shipped package manifest and all kernel/module/boot/configuration hashes. Root expansion, default login/sudo, owner-added root-key login, DHCP identity, NTP, fan, AppArmor/audit, four CPU timers and clean journal/services passed. No maintenance key was included in the image. A freshly written image contains only its shipped kernel; prepare a medium-specific backup before later kernel experiments.

These finite checks do not establish long-duration reliability or blanket peripheral acceptance. Local patches are not claimed as upstream-accepted changes. The complete source retains the inactive diagnostic code present in the tested binary; enabling diagnostics changes the test conditions.
