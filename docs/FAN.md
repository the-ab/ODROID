# U3 fan control

[Deutsch](FAN.de.md)

The kernel thermal governor controls the PWM fan. Defaults are **35 / 45 / 55 °C**, with **3 °C hysteresis** on cooling. Dedicated fan trips preserve the CPU's original throttling/critical protection.

| State | Rising temperature | PWM, 0–255 |
|---:|---:|---:|
| 0 | Below the first trip | 0 |
| 1 | 35 °C | 102 |
| 2 | 45 °C | 170 |
| 3 | 55 °C | 255 |

```sh
odroid-fan status
sudo odroid-fan set 40 50 60
odroid-fan status
```

`set` applies the thresholds immediately and saves them in `/etc/default/odroid-fan` for subsequent boots. Values must be integers from 30 to 85 °C in rising order with at least 5 °C between them. Restore defaults with:

```sh
sudo odroid-fan set 35 45 55
```

Alternatively edit `FAN_LOW`, `FAN_MEDIUM`, `FAN_HIGH` in the configuration and run `sudo systemctl restart odroid-fan.service`. Invalid values are refused. Changing fan trips does not change CPU protection trips.

`status` reports current temperature, active/configured trips, cooling state and PWM. RPM is not exposed by this hardware configuration. PWM is a duty setting, not a measured rotation speed. On cooling, hysteresis means a higher state can remain active below its rising threshold.
