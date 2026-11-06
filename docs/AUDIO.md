# U3 analog audio

[Deutsch](AUDIO.de.md)

The U3 uses the MAX98090 codec. Earlier kernels passed physical 48 kHz/S16 stereo headphone playback with both channels confirmed audible. The current v32 internal stereo loop passed and the former I2S RX-DMA warning is corrected. Physical microphone speech and current v32 headphone listening remain separate acceptance steps.

The SSH image need not include a desktop audio server. Install ALSA tools if needed:

```sh
sudo apt update
sudo apt install alsa-utils
aplay -l
amixer -c 0 sget Headphone
sudo alsactl --no-ucm -f /path/to/before.state store 0
amixer -c 0 -- sset Headphone -20dB
```

The `--` is needed before the command so a negative dB value is not parsed as an option. Test with a low-level file using `aplay -D plughw:0,0 FILE.wav`; do not start at maximum volume. The verified routing uses `MIXHPLSEL Mux`/`MIXHPRSEL Mux` set to `DAC Only` and both headphone switches enabled. `odroid` already belongs to the audio group. `alsactl --no-ucm` stores/restores direct mixer controls without requiring a board UCM profile. Desktop PipeWire/PulseAudio, microphone routing and other devices require their own acceptance. Test mixer settings were restored afterwards; a working snapshot was retained privately.

The [platform corrections](I2S-USB.md) explain the stream-specific DMA requests and capture graph. Internal full duplex does not prove that an attached headset microphone, its wiring or the external analog input works.
