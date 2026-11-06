# U3-Grafik

[English](GRAPHICS.md)

Exynos-Anzeigecontroller und Mali-GPU sind getrennte Geräte. Der Kernel aktiviert Exynos-DRM/HDMI und Lima für alle vier Mali400-Pixelprozessoren. Bei Installation grafischer Pakete liefert Ubuntu Mesa den Userspace-Treiber. Die beiden SSH-Images installieren und starten keinen Desktop.

[Mesa Lima](https://docs.mesa3d.org/drivers/lima.html) unterstützt GLES2 und begrenztes Desktop-OpenGL 2.1. GLES3, Desktop-GL3+ und Vulkan stehen bei dieser GPU nicht zur Verfügung. Erfolgreiche GLES2-Tests bestätigen keine Programme, die neuere APIs voraussetzen.

Die Prototyp-Prüfung mit Mesa 26.0.8 bestätigte Mali400-Hardware-Rendering, insgesamt 1.440 geprüfte Shader-Farbstichproben als root/odroid, einen vollständigen direkten DRM-Lauf über 328 Sekunden bei 1920×1080 und Xorg-Glamor/direktes GLX mit rund 60 FPS in glxgears bei VSync. Höchste CPU-Temperatur in diesem direkten Lastlauf: 42 °C, keine neuen Kernelmeldungen. Beim ersten Xorg-Test nach dem HDMI-Trennen wurde ein 1024×768-Connector erzwungen.

Am 30.10.2026 bestätigte der Test mit wieder angeschlossenem HDMI gültige 256-Byte-EDID und native **1920×1080 bei 60 Hz**. Xorg modesetting/Glamor/direktes GLX und Westons **DRM-Backend mit GL-Renderer** renderten als normaler Benutzer odroid auf Mali400. Der Nutzer bestätigte beide tatsächlichen HDMI-Bilder als sichtbar und fehlerfrei. X11-Zahnräder liefen mit rund 60 FPS; natives Wayland bestand im Fenster und Offscreen jeweils alle 27 Szenen mit festem Referenzwert, bei jeweils sechs nicht eindeutig vergleichbaren Szenen. Zusätzliche Wayland-Last war erfolgreich; höchste CPU-Temperatur über die angeschlossenen Tests: 43 °C. Keine Kernel-/Journalwarnungen oder -fehler. Der Prototyp blieb bei `6.12.114-odroidu3-test4`; minimal v1 bestand anschließend native eMMC-Basisprüfungen. Rendering auf dem tatsächlichen v1-Kernel und andere neue Image-Startwege bleiben von diesen Prototyp-Grafikergebnissen getrennt.

Für Grafikprüfungen beispielsweise die benötigten Pakete installieren:

```sh
sudo apt update
sudo apt install --no-install-recommends mesa-utils libgl1-mesa-dri libegl-mesa0 \
  libgbm1 libgles2 libdrm-tests kmscube glmark2-es2-wayland weston \
  xserver-xorg-core xserver-xorg-input-libinput xinit x11-xserver-utils
id
```

Der Image-Benutzer gehört zu `video` und `render`. In einer gestarteten grafischen Sitzung mit `glxinfo -B` oder `eglinfo -B` prüfen: Für GPU-Beschleunigung muss der Renderer **Mali400** heißen, nicht llvmpipe/softpipe.

Im geprüften Weston-Headless-GL-Aufbau führte die automatische Gerätewahl zu `DRM_IOCTL_MODE_CREATE_DUMB ... Permission denied` und Client-Abstürzen. Ausdrückliche Auswahl der Mali behebt diesen getesteten Pfad:

```sh
odroid-gpu glmark2-es2-wayland --validate
```

`odroid-gpu BEFEHL ...` setzt für Programm/Sitzung `DRI_PRIME=platform-13000000_gpu`. Damit bestehen Fenster- und Offscreen-Prüfung alle 27 Szenen mit Referenzwerten. Sechs Szenen bieten keinen eindeutigen Vergleich; Terrain benötigt fehlendes Vertex-Texture-Fetching. Das ist ein geprüfter Workaround, keine Abnahme beliebiger Wayland-Compositors.

Der native Weston-Test verwendete dieselbe Gerätewahl für Compositor und Clients, mit Exynos-Anzeigegerät `card1`, DRM-Backend und GL-Renderer. Die kleine Testinstallation protokollierte fehlende Drag-and-drop-Cursornamen; eine vollständige Desktopumgebung einschließlich Theme-Integration war nicht Gegenstand des Tests. Temporäre Grafiksitzungen wurden beendet und die bisherige Textkonsole wiederhergestellt. Ein grafischer Autostart wurde nicht eingerichtet.

glmark2 erzwingt im [Hauptprogramm für die Validierung 800×600](https://github.com/glmark2/glmark2/blob/2023.01/src/main.cpp#L184); das [direkte DRM-Backend verwendet aber die native Anzeigegröße](https://github.com/glmark2/glmark2/blob/2023.01/src/native-state-drm.cpp#L97). Referenzfehler einer nativen 1920×1080-Validierung sind deshalb kein gültiger Vergleich. Einen tatsächlichen 800×600-Fenster-/Offscreen-Pfad verwenden.

MFC-Videodekodierung und vollständige Desktopumgebungen wurden damit nicht geprüft. Siehe [Hardwarestand](HARDWARE.de.md).
