# Releases

[Deutsch](RELEASES.de.md)

The source and kernel release for image recipe **1.0.3** uses `7.3.1-odroidu3-v32`, DEB version `7.3.1-33` and activation tools `1.0.3`. [Kernel release](https://github.com/the-ab/ODROID/releases/tag/u3-kernel-7.3.1-33) · [APT packages](https://the-ab.github.io/deb/) · [Validation](CANDIDATE-1.0.3.md).

**Full image ZIPs are held in a draft, not public downloads.** The reference-derived BL1/BL2/TrustZone bytes have pinned hashes, but their exact redistribution/source coverage remains unresolved. Hash provenance is not a license grant. The separate kernel DEBs and corresponding-source bundle contain no vendor boot blobs. A firmware-free local-assembly kit would be a different deliverable requiring its own validation; it is not silently substituted for the tested images.

Published packages identify the recipe/source commit, configuration, patch, checksums and exact matching Linux source archive. Full image releases additionally require their package manifests, IMG/ZIP hashes, filesystem/partition/boot readback, full ZIP roundtrip, absence of private access keys/identities and documented firmware coverage. Hardware evidence must distinguish each variant and boot medium. See [hardware status](HARDWARE.md).

The compiled v32 kernel passed the documented native boot/server qualification. Fresh minimal 1.0.3 passed native-eMMC basic checks; minimized/SD first boots, current physical graphics/microphone and unexercised peripherals remain open and must not be represented as accepted. Build-time tests do not replace physical boot checks.

Image versions use SemVer; kernel versions retain the upstream version and board revision. Changed compiled bytes require a new board suffix. Repacking documentation can change a ZIP checksum while preserving the IMG hash; use the checksum shipped with that particular archive. Existing releases and matching-source history remain intact. Publication is deliberate, never triggered automatically by a build script.
