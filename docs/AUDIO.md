# U3 analog audio

[Deutsch](AUDIO.de.md)

MAX98090 headphone playback was accepted on 7.3.1-odroidu3-v1:48 kHz,16-bit stereo, left/right tones as ordinary `odroid`, both channels explicitly confirmed by the user. Kernel 7 logs an I2S RX-DMA warning(-19); it did not prevent playback. Microphone/capture is not accepted by this output-only test.

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
