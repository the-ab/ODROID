# U3-Grafik

[English](GRAPHICS.md)

Exynos-Anzeigecontroller und Mali-GPU sind getrennte Geräte. Der Kernel aktiviert Exynos-DRM/HDMI und Lima für alle vier Mali400-Pixelprozessoren. Bei Installation grafischer Pakete liefert Ubuntu Mesa den Userspace-Treiber. Die beiden SSH-Images installieren und starten keinen Desktop.

[Mesa Lima](https://docs.mesa3d.org/drivers/lima.html) unterstützt GLES2 und begrenztes Desktop-OpenGL 2.1. GLES3, Desktop-GL3+ und Vulkan stehen bei dieser GPU nicht zur Verfügung. Erfolgreiche GLES2-Tests bestätigen keine Programme, die neuere APIs voraussetzen.

Die Prototyp-Prüfung mit Mesa 26.0.8 bestätigte Mali400-Hardware-Rendering, insgesamt 1.440 geprüfte Shader-Farbstichproben als root/odroid, einen vollständigen direkten DRM-Lauf über 328 Sekunden bei 1920×1080 und Xorg-Glamor/direktes GLX mit rund 60 FPS in glxgears bei VSync. Höchste CPU-Temperatur unter direkter Grafiklast: 42 °C, keine neuen Kernelmeldungen. Nach absichtlichem HDMI-Trennen durch den Nutzer lief Xorg mit erzwungenem 1024×768-Connector. Ein echter Monitor-Desktopbetrieb und die neuen v1-Images sind noch abzunehmen.

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

glmark2 erzwingt im [Hauptprogramm für die Validierung 800×600](https://github.com/glmark2/glmark2/blob/2023.01/src/main.cpp#L184); das [direkte DRM-Backend verwendet aber die native Anzeigegröße](https://github.com/glmark2/glmark2/blob/2023.01/src/native-state-drm.cpp#L97). Referenzfehler einer nativen 1920×1080-Validierung sind deshalb kein gültiger Vergleich. Einen tatsächlichen 800×600-Fenster-/Offscreen-Pfad verwenden.

MFC-Videodekodierung und vollständige Desktopumgebungen wurden damit nicht geprüft. Siehe [Hardwarestand](HARDWARE.de.md).
