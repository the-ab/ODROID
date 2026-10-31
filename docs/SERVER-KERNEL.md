# U3 server kernel profile

[Deutsch](SERVER-KERNEL.de.md)

Linux **7.3.1-odroidu3-v3**, Debian version **7.3.1-4**, is the full server profile used by fresh image **1.0.2**. The earlier 6.12 and 7.3.1-v1 configurations were hardware bring-up baselines and did not cover this full service scope. Existing installed kernels remain local recovery options.

The complete resolved configuration is [kernel.config](../boards/u3/kernel.config). The build and package gates require [101 capabilities](../boards/u3/server-requirements.json); a missing required option fails the build. `y` means built in; `m` means supplied as a loadable module. Kernel capability does not install or configure the corresponding server application.

| Area | Included capabilities | Qualification |
|---|---|---|
| Containers | Namespaces, cgroup v2 CPU/memory/PID/I/O controllers, seccomp, cgroup BPF, overlayfs, bridge/veth, NAT | Docker29: native ARM container, DNS, bridge, published port, overlay persistence, volume, resource limits, AppArmor and seccomp |
| Network/firewall | IPv4/IPv6, conntrack, nftables, iptables, ipset, VLAN, bonding, macvlan/ipvlan, VXLAN, policy routing, QoS | nftables stateful allow/reject and counters, IPv4/IPv6 traffic, iptables-nft rules |
| VPN | WireGuard, TUN/TAP, XFRM/IPsec crypto and tunnel support | WireGuard encrypted handshake/data; OpenVPN2.7 TLS/AES-GCM TUN data. IPsec and OpenVPN DCO are not qualified |
| File services | Kernel NFS client/server, CIFS/SMB client, FUSE, ACL/xattr/quota, inotify/fanotify | NFS4.2 server/client, encrypted SMB3.1.1 CIFS and authenticated Samba, SSHFS; read/write SHA256 checks |
| Storage | ext4, XFS, Btrfs, F2FS, exFAT, NTFS3, ISO/UDF/EROFS, loop/NBD, MD RAID, device mapper/LVM/thin/crypt/verity/integrity | Native ext4/eMMC file I/O; additional filesystem/storage modules load. No RAID, encrypted-root or external-disk workload acceptance |
| Security | AppArmor, Landlock, Yama, audit, SYN cookies, hardened usercopy, FORTIFY, W^X, stack protector, stack zeroing, slab freelist and list hardening | Actual AppArmor and Landlock denials, audit syscall event, Docker AppArmor/seccomp. Memory hardening verified in the running config |
| Diagnostics/memory | Socket diagnostics, tracing/kprobes/syscalls, task/scheduler stats, PSI, zram/zswap, optional pstore backend, watchdog | Socket/trace/pressure availability and module loading; short CPU/RAM/storage smoke test |
| Devices | Existing U3 eMMC/SD/Ethernet/USB/audio/DRM/fan support; FTDI, CP210x, PL2303 USB serial | U3 boot/network/fan confirmed. USB serial modules load; attached adapters are not claimed tested |

Core service tests run in isolated network/mount namespaces with temporary configurations. They exercise real kernel paths and payload transfers without replacing the board's LAN firewall or SSH service. Test daemons and temporary exports are removed afterwards. This is qualification of the listed paths, not a long-duration reliability or performance guarantee.

Boot files follow the usual flat layout: `/boot/vmlinuz-<release>`, `/boot/uImage-<release>`, `/boot/config-<release>`, `/boot/System.map-<release>` and `/boot/exynos4412-odroidu3-<release>.dtb`. Extlinux selects the versioned files; `/boot/uImage` remains the active legacy compatibility copy. No initramfs is required for the shipped unencrypted ext4 root. See [APT updates and recovery](KERNEL-UPDATES.md).

Fresh images enable AppArmor and auditd. Boot uses `audit=1 audit_backlog_limit=8192 psi=1`, preventing the early default64-entry backlog overflow observed during testing. A missing Ubuntu downstream `kernel.apparmor_restrict_unprivileged_userns` sysctl is marked optional: upstream AppArmor works, but that Ubuntu-specific restriction is **not** claimed enforced. The optional empty cron argument is defined to avoid its warning.

Limits: Cortex-A9 provides no usable KVM virtualization for this board; no BTF/CO-RE or complete eBPF application compatibility claim; no enforced verified-boot/module-signature trust chain; encryption modules do not provide a tested encrypted-root/initramfs installer; pstore availability does not reserve persistent RAM. BBR is optional, CUBIC remains the default. Hardware graphics/audio acceptance from earlier profiles does not automatically accept a complete desktop or every peripheral on v3. See [security review](SECURITY-REVIEW.md), [hardware](HARDWARE.md) and [release gates](RELEASES.md).

Native v3 Docker, VPN, firewall, file-service and security regression passed; fresh-image results are recorded separately in the release validation. A compiled option or locally validated ZIP alone is not physical image first-boot acceptance.
