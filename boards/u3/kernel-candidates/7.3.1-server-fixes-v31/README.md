# Combined U3 server fixes, revision31

[Deutsch](README.de.md)

This candidate combines the unchanged v30 GIC RAM-counter accessor correction and seven io_uring fixes with four reviewed v7 audio/USB changes: stream-specific Samsung DMA allocation, the physical microphone/backend route, playback-only HDMI capability and optional USB PHY VBUS acquisition with real errors propagated. The upstream secondary I2S topology is retained; no added parent relationship.

V30 passed its transition and three diagnostic warmboots, then one normal release-argument boot without diagnostic output. That normal boot still reproduced the old RX-DMA and missing-VBUS warnings because the isolation baseline had not incorporated the audio/USB fixes. The required ten warm/five halt-cold starts will therefore qualify this complete candidate. No new register masks, secure/debug/firmware changes, forced IRQ count or global JUMP_LABEL disable. All XFS/server capabilities remain. Source/build/package, native acceptance and physical microphone/display acceptance stay separate. V25 remains the exact direct rollback, v17 the reserve. No release acceptance.

The24-file pinned-source replay, ARM build,101-capability gate and actual C resource/compiled-DT audio graph checks pass. The DTB is byte-identical to functionally tested v7. Configuration changes only LOCALVERSION; package/native qualification remains open.
