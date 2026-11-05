# U3 TUN statistics correction, revision32

[Deutsch](README.de.md)

V31 passed ten pure warmboots and five controlled halt/cold starts with normal release arguments. Ordinary Docker, WireGuard/OpenVPN, firewall, file-service, security and internal codec data tests completed, but OpenVPN exposed a lockdep IRQ-context warning in per-CPU TUN statistics. This rejects final qualification despite successful transfers. No actual deadlock was observed. The NFS test also omitted its client-recovery daemon; that fixture issue is tracked separately.

The signed upstream32-bit u64_stats contract requires write-side exclusion against interrupt-context users. TUN has three process-context counter updates guarded only by preempt_disable(), while an existing XDP sender updates the same statistics with bottom halves disabled. The common network statistics lock class also covers USB softirq completions, matching the captured warning. This local candidate changes exactly those three short counter sections to local_bh_disable()/local_bh_enable(); copies and packet handling remain outside them. It preserves all v31 fixes and configuration except LOCALVERSION. Lockdep stays enabled. The exact underlying GIC text-patch/cache mechanism remains unproven.

Package verification, fresh native warning/lockdep checks and normal boot/service qualification remain pending. V25 stays the exact direct rollback, v17 the reserve; v31 evidence/debug/reinstall bytes are retained. No firmware change or public binary/APT/Main promotion.

The25-file pinned-source replay, resolved configuration,101-capability check and ARM kernel/module build pass. The DTB remains byte-identical to v31. Package/native verification remains pending.
