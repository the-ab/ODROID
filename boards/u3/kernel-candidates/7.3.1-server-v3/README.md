# U3 Linux7.3.1 server revision3

Explicit server profile, release7.3.1-odroidu3-v3/package7.3.1-3. Same verified upstream and five board patches as v1; the configuration adds container storage/network/cgroup controllers, nftables/iptables, VPN, file-service/storage modules, AppArmor/Landlock/audit and additional memory/network hardening. Hardware boot support and fan35/45/55 remain inherited. The original1.0.1 image recipe and published v1 packages remain immutable.

Native Docker, VPN, firewall and file-service qualification is required before claiming support. A configuration option does not prove a live service works. Compile only from the pinned archive with this full config and patch. Many service drivers are modules, while security policy and CPU/memory controllers are built in. Some historical Kconfig symbols have changed upstream; requested-options.json records requests, while kernel.config is authoritative. This profile does not publish itself.

Additional audit adds common removable filesystems, USB serial, network diagnostics/QoS, optional storage verification/encryption support and slab/list/stack hardening. Native v2 and v3 service tests passed; see docs/SERVER-KERNEL.md for the tested scope. Audit startup uses audit=1 audit_backlog_limit=8192 in new images.
