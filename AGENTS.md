# Working on ODROID

Read README, the relevant board JSON/config and docs/HARDWARE before changing recipes. Keep board-specific code under its board directory. XU4 is planned and must not inherit U3 boot offsets or hardware acceptance.

Use separate, marked build directories outside the repository. Never copy a running installation into a universal release. Keep private keys, authorized keys, runtime identities, personal host/IP/CID data, raw logs and binary image/build caches out of Git. Standard numeric filesystem ownership and modes belong in images; shared workspace ACLs do not.

Image assembly writes regular files only. Firmware tooling defaults to inspection; a real boot0 write requires an explicitly selected device, same-module verified backup, payload checksum, CID confirmation and the documented adapter path. Analysis-only hardware remains read-only unless the user separately authorizes changes.

Relevant checks are Python compilation, shellcheck, boot0 failure/rollback tests, fresh ARM rootfs QA, complete image readback and ZIP roundtrip. Record source, image and actual hardware acceptance separately. Do not claim an unbooted image or untested peripheral is accepted. Keep one writer per checkout and preserve unrelated work.

Document changes in English `.md` and German `.de.md`. Binary releases require complete matching sources/licenses, checksums and explicit release approval. Do not publish candidates automatically from a build script.
