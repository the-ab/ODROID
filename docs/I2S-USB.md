# U3 platform corrections

[Deutsch](I2S-USB.de.md)

The shipped v32 profile keeps the following reviewed local changes in the canonical `boards/u3/patches/platform.patch`. They are not claimed as upstream-accepted fixes.

- Samsung I2S requests only the DMA directions present on each primary/secondary interface. The U3 capture graph names the primary endpoint, preserving playback and capture ownership.
- The HDMI DAI advertises playback only. Optional USB VBUS regulators propagate real provider/defer errors while accepting an absent optional supply; USB reset and power boundaries remain intact.
- MMC voltage selection rejects inverted ranges and propagates failed supported-voltage queries before the regulator API. This is a secondary error-path correction, not evidence that MMC caused the original stall.
- The non-banked GIC accessor selects its per-CPU register base using the initialized RAM key counter. Failed controls captured an incorrect original base/range selection; healthy alias/cross-CPU controls were checked separately. The exact text-patching/cache mechanism remains unproven. No speculative IRQ masks, secure/debug unlocks or guessed MMIO writes are used.
- Three process-context TUN statistics sections exclude softirq writers. Lockdep stays enabled; OpenVPN/TUN and full server regression passed after this correction.

The final v32 kernel passed ten pure warmstarts and five controlled halt/cold starts with normal arguments. Each start checked four advancing CPU timers, 351 module hashes, boot/configuration payloads and health. Full server tests, ordinary non-root io_uring, Ethernet transfer and the internal stereo codec loop passed with no new kernel warnings. Earlier I2S RX-DMA and absent optional-VBUS warnings no longer occur.

Physical headset playback was accepted on earlier revisions; physical microphone input remains unconfirmed. No boot0, boot1 or EXT_CSD change was part of these kernel fixes. Driver support and finite tests do not establish blanket peripheral or long-duration acceptance. See [hardware status](HARDWARE.md), [audio](AUDIO.md) and [security](SECURITY-REVIEW.md).

Obsolete experimental profiles were removed from the current source tree. The [Git history](https://github.com/the-ab/ODROID/commits/main/) retains the investigation and matching sources; the canonical patch retains the code used by the released binary. UART diagnostics, if needed for new work, require the board's 1.8 V interface and a checked connector orientation. See [Hardkernel's U3 specifications](https://www.hardkernel.com/shop/odroid-u3/).
