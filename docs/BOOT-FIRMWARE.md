# U3 boot firmware: origin and license review

[Deutsch](BOOT-FIRMWARE.de.md)

Reviewed 6 November 2026. Startup follows `Exynos iROM -> BL1 -> BL2 / TrustZone -> U-Boot -> Linux -> Ubuntu`. BL1 loads the next stage, BL2 performs early board/DRAM initialization, and TrustZone supports the secure processor world. These are separate from our Linux kernel and Ubuntu root filesystem.

## Exact origin

The pinned [U-Boot U3/X2 instructions](https://github.com/u-boot/u-boot/blob/v2026.10/doc/README.odroid#L25-L32) link [boot.tar.gz](https://odroid.in/guides/ubuntu-lfs/boot.tar.gz). Archive: 174080 bytes, SHA256 `e0db737d9e49f937425e4778b0ab892623bcc389d7c26329ba2e97ae7bb475c4`.

| Stored image component | Bytes | SHA256 |
|---|---:|---|
| BL1 | 15360 | `0fcf68a3ff3e47af7c6d91103d5797e4aefbefd32b1d267daff69eb6e69d2a84` |
| BL2 | 14848 | `7b1bab8c9ee7d495ab75b2e0a7a0c6295c13f06c86320c25ba379f47d0ec3b57` |
| TZSW | 159744 | `777e0efdd626863b2a6e83cd24b42ae028158aecbfec7843dad00f1b458958c3` |

`boot/E4412_S.bl1.HardKernel.bin` and `boot/E4412_S.tzsw.signed.bin` match exactly. The first 14848 bytes of `boot/bl2.signed.bin` match BL2; its remaining 1536 bytes are zero. Including the following zero-filled image gap reproduces the complete official 16384-byte BL2, SHA256 `8f459e654ec4c1a33185ba3f8e04a13da8c6def79362948a6648f96c48897015`. No nonzero content was omitted.

## Remaining evidence

The archive contains three boot binaries, an older U-Boot and `sd_fusing.sh`, with no separate binary license. The script has a Samsung GPL-2 notice. Public download availability and that script notice are not treated as a redistribution/source statement for adjacent binaries. No inspected material explicitly grants redistribution of these exact binaries, and the older signed BL2's corresponding-source mapping remains unresolved. This is a missing-evidence finding, not a determination that redistribution is prohibited or all three files are proprietary.

Hardkernel's [XU4 discussion](https://github.com/hardkernel/u-boot/issues/49#issuecomment-464464173) and [C2 permission](https://github.com/hardkernel/u-boot/issues/39#issuecomment-296126525) concern different boards; neither is applied as a U3 grant. The inspected [website/order terms](https://www.hardkernel.com/agreement/) provide no identified U3 firmware grant. Our new U-Boot source release does not identify the older BL2's source.

Project release conditions therefore keep complete image ZIPs and the boot0 repair prefix unpublished until suitable terms/source coverage are documented. Kernel DEBs contain no such boot binaries and are available through signed APT. A separately implemented download kit could omit these components and insert them locally from an authorized reference; that would require exact reassembly checks and clear instructions. The tested full IMG is not silently replaced by a different format.
