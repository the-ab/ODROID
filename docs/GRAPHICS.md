# U3 graphics

[Deutsch](GRAPHICS.de.md)

The Exynos display controller and Mali GPU are separate devices. The kernel enables Exynos DRM/HDMI and Lima for all four Mali400 pixel processors. Ubuntu Mesa supplies the user-space driver when graphical packages are installed. The two SSH image variants do not install or autostart a desktop.

The [Mesa Lima documentation](https://docs.mesa3d.org/drivers/lima.html) describes GLES2 and limited desktop OpenGL 2.1 support. This GPU does not provide GLES3, desktop GL3+ or Vulkan. A modern application requiring those APIs is not covered by successful GLES2 tests.

Prototype tests with Mesa 26.0.8 confirmed Mali400 hardware rendering, 1,440 checked shader samples across root/odroid tests, a complete 328-second direct DRM run at 1920×1080, and Xorg Glamor/direct GLX with glxgears around 60 FPS under VSync. Maximum CPU temperature during that direct load was 42 °C; no new kernel messages occurred. The initial Xorg check used a forced 1024×768 connector after HDMI was disconnected.

Connected-HDMI testing on 2026-10-30 confirmed valid 256-byte EDID and native **1920×1080 at 60 Hz**. Xorg modesetting/Glamor/direct GLX and Weston 14's **DRM backend with GL renderer** both rendered on Mali400 as the normal odroid user. The user confirmed both actual HDMI pictures were visible and free of display errors. X11 gears stayed around 60 FPS; native Wayland passed all 27 defined reference scenes in both windowed and offscreen tests, with six indeterminate scenes in each. Additional Wayland load passed; maximum CPU temperature across the connected tests was 43 °C. No kernel/journal warnings or errors occurred. The running prototype stayed on `6.12.114-odroidu3-test4`; minimal v1 subsequently passed native eMMC basic boot/runtime checks. Rendering on the actual v1 kernel and other new-image boot paths remain separate from these prototype graphics results.

For graphical testing, install the required packages, for example:

```sh
sudo apt update
sudo apt install --no-install-recommends mesa-utils libgl1-mesa-dri libegl-mesa0 \
  libgbm1 libgles2 libdrm-tests kmscube glmark2-es2-wayland weston \
  xserver-xorg-core xserver-xorg-input-libinput xinit x11-xserver-utils
id
```

The image account belongs to `video` and `render`. In an established graphical session, check `glxinfo -B` or `eglinfo -B`; a successful GPU result must say **Mali400**, not llvmpipe/softpipe.

The tested Weston headless GL path chose an unsuitable display-device allocation path by default, causing `DRM_IOCTL_MODE_CREATE_DUMB ... Permission denied` and client crashes. Selecting the Mali render device resolved this:

```sh
odroid-gpu glmark2-es2-wayland --validate
```

`odroid-gpu COMMAND ...` sets `DRI_PRIME=platform-13000000_gpu` for that application/session. Both windowed and offscreen validation then passed all 27 scenes with reference values; six scenes have no definite comparison. Terrain requires unsupported vertex texture fetching. This is a tested workaround, not a claim that every Wayland compositor has been validated.

The native Weston test used that same device selection for compositor and clients, with the Exynos display device `card1`, the DRM backend and GL renderer. Its small test installation logged missing drag/drop cursor-name warnings; a complete desktop environment and its theme integration were outside the test. Temporary display sessions were stopped and the original text console restored. No graphical autostart was installed.

glmark2's validation forces 800×600 in its [main program](https://github.com/glmark2/glmark2/blob/2023.01/src/main.cpp#L184); the [direct DRM backend uses native display dimensions](https://github.com/glmark2/glmark2/blob/2023.01/src/native-state-drm.cpp#L97). Reference failures from a native 1920×1080 validation run are therefore not valid comparisons. Use a real 800×600 window/offscreen validation path.

MFC hardware video decoding and complete desktop environments have not been tested by these rendering checks. See [hardware status](HARDWARE.md).
