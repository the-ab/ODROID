# U3 hardware verification

[Deutsch](HARDWARE.de.md)

Source/configuration support, prototype operation and acceptance of a new image are separate claims. On 2026-10-30, the **minimal v1.0.0 and v1.0.1** image booted from native 16 GB eMMC with **6.12.114-odroidu3-v1**. Stock odroid password login and sudo, root expansion, stable Ethernet identity, network time, fan thresholds, matching boot-file hashes and exact package versions passed. No journal errors or failed units occurred. Minimized and new-image SD boot remain separate open checks.

| Component | Evidence / limit |
|---|---|
| SD and native eMMC | Minimal v1.0.0 passed native eMMC first boot and basic runtime checks. Earlier prototypes booted SD and native eMMC; boot0 repair was accepted on two 16 GB SDW16G modules. A normal reader write covers the user area only. |
| CPU/RAM/storage/network | Earlier prototype stability run passed CPU/memory load, memory patterns, file write/direct-read hash checks and network transfer. GPU tests did not replace those checks. |
| Ethernet identity | Hardware-derived locally administered MAC stayed stable across SD/eMMC; the driver-supplied permanent address takes precedence. |
| Fan/thermal/power key | Four fan states observed; configurable dedicated trips 35/45/55 °C, CPU protection retained; clean power-key shutdown confirmed. |
| Pin controller | Consumed wakeup-IRQ fwnode link fix removed the preceding device-link error in actual SD/eMMC boots. |
| Mali/HDMI/X11/Wayland | See [graphics](GRAPHICS.md). Connected HDMI at 1080p60 with Xorg and native Weston DRM/GL confirmed, including the user's visual acceptance. New v1 images and complete desktop environments retain separate acceptance. |
| USB, input, GPIO/I²C/SPI, RTC | Drivers enabled. Only the actually exercised USB/network/input paths are confirmed; no blanket peripheral acceptance. |
| MAX98090 audio / Samsung MFC video | Kernel support and MFC firmware included; physical audio and hardware decoding not validated. |
| XU4 | Planned, no image or hardware verification yet. |

Kernel patches are local changes, not claimed as upstream-accepted fixes: hardware serial export, dedicated fan trips/invalid OPP exclusion, Exynos EHCI PHY lifecycle, DWC2 hardware defaults and consumed wakeup-IRQ link cleanup/diagnostics. The v1 DTB matches the preceding DTB byte for byte. The minimal image has now passed native eMMC basic boot/runtime checks; this does not transfer to every variant, boot path or peripheral.

The image contains no personal fixed MAC, host key or maintenance authorized key. The same image can be written to another U3 and derives that board's identity. MAC derivation is a deterministic fallback, not a claim that the LAN chip has a programmed factory EEPROM address.

The minimal first boot logged known platform/lockdep and absent optional-camera messages, plus an unset optional cron `EXTRA_OPTS` variable. Cron remained active with result success; no pin-controller device-link error recurred. The cron warning is tracked for a later recipe cleanup.

Minimal 1.0.1 native-eMMC follow-up passed: the owner added a root public key and confirmed login; SSH journal evidence matched, the shipped key-only policy was effective without a local override and root remained password-locked. Kernel/meta/tools/keyring packages, all module/payload/boot hashes and the complete image package manifest matched. Board/media/payload admission checks passed without activation. The configured APT endpoint was reachable from the board and its downloaded signature verified against key bytes identical to the installed archive key. Lists are currently empty. No live cache refresh, package upgrade or configuration change was performed; an actual different-kernel upgrade/boot remains pending.
