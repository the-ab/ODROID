# U3 hardware verification

[Deutsch](HARDWARE.de.md)

Source/configuration support, prototype operation and acceptance of a new image are separate claims. Current v1 candidates have not yet been physically booted. The kernel patch set was exercised in the preceding 6.12.114 prototype.

| Component | Evidence / limit |
|---|---|
| SD and native eMMC | Prototype booted both paths; native boot0 repair accepted on two 16 GB SDW16G modules. A normal reader write covers the user area only. |
| CPU/RAM/storage/network | Earlier prototype stability run passed CPU/memory load, memory patterns, file write/direct-read hash checks and network transfer. GPU tests did not replace those checks. |
| Ethernet identity | Hardware-derived locally administered MAC stayed stable across SD/eMMC; the driver-supplied permanent address takes precedence. |
| Fan/thermal/power key | Four fan states observed; configurable dedicated trips 35/45/55 °C, CPU protection retained; clean power-key shutdown confirmed. |
| Pin controller | Consumed wakeup-IRQ fwnode link fix removed the preceding device-link error in actual SD/eMMC boots. |
| Mali/HDMI/X11/Wayland | See [graphics](GRAPHICS.md). Hardware rendering confirmed; physical desktop output and new-image acceptance remain open. |
| USB, input, GPIO/I²C/SPI, RTC | Drivers enabled. Only the actually exercised USB/network/input paths are confirmed; no blanket peripheral acceptance. |
| MAX98090 audio / Samsung MFC video | Kernel support and MFC firmware included; physical audio and hardware decoding not validated. |
| XU4 | Planned, no image or hardware verification yet. |

Kernel patches are local changes, not claimed as upstream-accepted fixes: hardware serial export, dedicated fan trips/invalid OPP exclusion, Exynos EHCI PHY lifecycle, DWC2 hardware defaults and consumed wakeup-IRQ link cleanup/diagnostics. The v1 DTB matches the tested preceding DTB byte for byte; its newly built kernel and fresh rootfs still require their own boot checks.

The image contains no personal fixed MAC, host key or maintenance authorized key. The same image can be written to another U3 and derives that board's identity. MAC derivation is a deterministic fallback, not a claim that the LAN chip has a programmed factory EEPROM address.
