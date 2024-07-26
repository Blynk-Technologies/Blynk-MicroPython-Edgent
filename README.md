
# Blynk.Edgent for MicroPython

Blynk provides custom MicroPython builds specifically designed for IoT applications.
These builds offer a standard MicroPython environment, enriched with numerous fixes, improvements,
and additional features such as **secure Blynk.Cloud connection, device claiming and provisioning, OTA updates, configuration storage**, [and more](#features).

## Getting Started

- Sign up/Log in to your [Blynk Account](https://blynk.cloud)
- Install **Blynk IoT App** for iOS or Android

## 1. Install our `MicroPython` build

### ESP32

- Generic `ESP32`: 4MB / 8MB / 16MB Flash (PSRAM is auto-detected)
- Generic `ESP32-C3`: 4MB Flash
- Generic `ESP32-S3` (PSRAM is auto-detected):
  - Quad Flash: 8MB
  - Octa Flash: 8MB / 16MB
- `Seeed EdgeBox-ESP-100`: WiFi + Ethernet + Cellular
- `TTGO T-Internet-COM`: WiFi + Ethernet + Cellular
- `TTGO T-PCIE`: WiFi + Cellular
- `TTGO T-Call SIM800C`: WiFi + Cellular/2G

<a href="https://espressif.github.io/esp-launchpad/?flashConfigURL=https://vsh.pp.ua/Blynk-MicroPython-Edgent/esp-quickstart.toml">
    <img alt="Try it with ESP Launchpad" src="https://espressif.github.io/esp-launchpad/assets/try_with_launchpad.png" width="250">
</a>

### Raspberry Pi Pico W

1. Hold down the `BOOTSEL` button while plugging the board into a USB port
2. Copy the latest `UF2 firmware file` to the USB mass storage device that appears
3. Once programming of the new firmware is complete, the device will automatically reset and be ready for use

## 2. Connect your device to Blynk.Cloud

1. Open **Blynk IoT App** on your smartphone
2. Click **Add device** -> **Find devices nearby**
3. Select your device and follow the setup instructions

> [!NOTE]
> If you have already created your device in Blynk,
> you can [connect it manually using REPL](_extra/Cookbook.md#manual-device-connection)

## 3. Edit the default MicroPython app

The [`main.py`](./main.py) is a simple `asyncio`-based script that defines the high level device operation.
It could be as simple as this:

```py
from blynk import edgent
from time import ticks_ms
from asyncio import sleep_ms

async def publisher_task():
    while True:
        await sleep_ms(1000)
        edgent.updateDataStream("Uptime", ticks_ms())

edgent.run_asyncio_loop([
    publisher_task()
])
```

There are many ways to program your device. Here, we'll guide you through the two most popular options:

- [ViperIDE for Web and Mobile](_extra/Workflow-ViperIDE.md)
- [CLI using mpremote](_extra/Workflow-CLI.md)

# Features

- `blynk.inject` - BLE-assisted device claiming and provisioning
- `blynk.air` - OTA updates using **Blynk.Console** and **Blynk.Apps**
- `blynk.time` - Time Zone handling (including DST transitions), Sunrise/Sunset calculation
- `blynk.repl` - Remote MicroPyhton REPL for Blynk Terminal
- `netmgr` - Network management for `WiFi`, `Ethernet` and `Cellular`
- `config` - System-wide configuration
- `aiontp` - A versatile asyncio-based version of NTP client
- `logging` - System-wide, preconfigured logging
- `board` - A unified way to access the board peripherals
- Factory reset function
- Support for TLS certificate bundles
- For `ESP32`:
  - `coredump` - Collect crash reports remotely
  - OTA updates for MicroPython system firmware

# Further reading

- [Cookbook](_extra/Cookbook.md)
- [`asyncio` documentation](https://docs.micropython.org/en/latest/library/asyncio.html)
- [`asyncio` tutorial](https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md)
