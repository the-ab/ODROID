# U3-Serverkernel

[English](SERVER-KERNEL.md)

Linux **7.3.1-odroidu3-v3**, Debian-Version **7.3.1-3**, ist das vollständige Serverprofil für die frischen Images **1.0.2**. Die bisherigen 6.12- und 7.3.1-v1-Konfigurationen dienten der Hardware-Inbetriebnahme und deckten diesen Dienstumfang nicht vollständig ab. Bereits installierte Kernel bleiben als lokale Rückfallmöglichkeit erhalten.

Maßgeblich ist die vollständig aufgelöste [kernel.config](../boards/u3/kernel.config). Build und Paketierung prüfen [101 Pflichtfähigkeiten](../boards/u3/server-requirements.json); fehlt eine davon, bricht der Build ab. `y` bedeutet fest eingebaut, `m` ein mitgeliefertes ladbares Modul. Kernel-Unterstützung installiert oder konfiguriert noch keinen Serverdienst.

| Bereich | Enthalten | Prüfung |
|---|---|---|
| Container | Namespaces, cgroup-v2-CPU/Speicher/PID/I/O, Seccomp, cgroup-BPF, Overlayfs, Bridge/veth, NAT | Docker29: ARM-Container, DNS, Bridge, Portfreigabe, Overlay-Persistenz, Volume, Ressourcenlimits, AppArmor und Seccomp |
| Netzwerk/Firewall | IPv4/IPv6, Conntrack, nftables, iptables, ipset, VLAN, Bonding, macvlan/ipvlan, VXLAN, Policy-Routing, QoS | Zustandsabhängiges nftables-Erlauben/Abweisen mit Zählern, IPv4/IPv6-Verkehr, iptables-nft-Regeln |
| VPN | WireGuard, TUN/TAP, XFRM/IPsec-Krypto und Tunnel | Verschlüsselter WireGuard-Handshake/Daten, OpenVPN2.7 mit TLS/AES-GCM über TUN. IPsec und OpenVPN-DCO sind nicht abgenommen |
| Dateidienste | Kernel-NFS-Client/Server, CIFS/SMB-Client, FUSE, ACL/xattr/Quota, inotify/fanotify | NFS4.2-Server/Client, verschlüsseltes SMB3.1.1-CIFS und authentifiziertes Samba, SSHFS; Lesen/Schreiben mit SHA256 |
| Speicher | ext4, XFS, Btrfs, F2FS, exFAT, NTFS3, ISO/UDF/EROFS, Loop/NBD, MD-RAID, Device-Mapper/LVM/Thin/Crypt/Verity/Integrity | Native ext4/eMMC-Dateizugriffe; weitere Dateisystem-/Speichermodule laden. Kein RAID-, verschlüsseltes Root- oder externer Datenträger-Lasttest |
| Sicherheit | AppArmor, Landlock, Yama, Audit, SYN-Cookies, Hardened-Usercopy, FORTIFY, W^X, Stackschutz/-nullung, Slab-Freelist- und Listenhärtung | Tatsächliche AppArmor-/Landlock-Zugriffsverweigerung, Audit-Syscall-Ereignis, Docker-AppArmor/Seccomp. Speicherhärtung in laufender Konfiguration geprüft |
| Diagnose/Speicher | Socketdiagnose, Tracing/Kprobes/Syscalls, Task-/Schedulerstatistik, PSI, zram/zswap, optionales Pstore-Backend, Watchdog | Socket-/Trace-/Pressure-Verfügbarkeit und Modulladen; kurzer CPU/RAM/Dateizugriff-Lasttest |
| Geräte | Bestehende U3-eMMC/SD/Ethernet/USB/Audio/DRM/Lüfter-Unterstützung; FTDI, CP210x, PL2303 | U3-Boot, Netzwerk und Lüfter bestätigt. USB-Seriell-Module laden; angeschlossene Adapter nicht als getestet ausgegeben |

Die Diensttests verwenden getrennte Netzwerk-/Mount-Namespaces und temporäre Konfigurationen. Sie prüfen reale Kernelpfade und Datenübertragungen, ohne LAN-Firewall oder SSH-Dienst des Boards zu ersetzen. Testprozesse und temporäre Exporte werden danach entfernt. Dies ist die Prüfung der genannten Funktionen, keine Langzeit- oder Leistungsgarantie.

Die Dateien liegen flach unter `/boot`: `vmlinuz-<release>`, `uImage-<release>`, `config-<release>`, `System.map-<release>` und `exynos4412-odroidu3-<release>.dtb`. Extlinux wählt die versionierten Dateien; `/boot/uImage` bleibt die aktive Kompatibilitätskopie. Das mitgelieferte unverschlüsselte ext4-Root benötigt keine Initramfs. Siehe [APT und Rückfall](KERNEL-UPDATES.de.md).

Frische Images aktivieren AppArmor und auditd. `audit=1 audit_backlog_limit=8192 psi=1` verhindert den im Test beobachteten Überlauf der frühen Standardwarteschlange mit64 Einträgen. Das fehlende Ubuntu-spezifische `kernel.apparmor_restrict_unprivileged_userns` wird als optional markiert: Upstream-AppArmor funktioniert, diese zusätzliche Ubuntu-Einschränkung wird jedoch **nicht** als wirksam behauptet. Die optionale leere Cron-Variable wird definiert.

Grenzen: Cortex-A9 bietet hier keine nutzbare KVM-Virtualisierung; keine BTF/CO-RE- oder vollständige eBPF-Anwendungskompatibilitätszusage; keine erzwungene Verified-Boot-/Modulsignatur-Vertrauenskette; Verschlüsselungsmodule ersetzen keinen geprüften Encrypted-Root-/Initramfs-Installer; Pstore-Unterstützung reserviert keinen persistenten RAM. BBR bleibt optional, CUBIC Standard. Frühere Grafik-/Audioabnahmen ersetzen keine vollständige Desktop-/Peripherieabnahme auf v3. Siehe [Sicherheit](SECURITY-REVIEW.de.md), [Hardware](HARDWARE.de.md) und [Releasebedingungen](RELEASES.de.md).

Die nativen v3-Prüfungen für Docker, VPN, Firewall, Dateidienste und Sicherheit bestanden; neue Imageprüfungen werden separat im Release-Nachweis erfasst. Eine kompilierte Option oder lokal geprüfte ZIP bestätigt keinen physischen Erststart dieses Images.
