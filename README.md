
# Blynk.Edgent for MicroPython

Blynk offers custom MicroPython builds tailored for IoT applications.
These builds provide a standard, MicroPython environment enhanced with various fixes, improvements,
and additional features like device claiming and provisioning, OTA updates, configuration store and [many more](#features).

## Getting Started

- Sign up/Log in to your [Blynk Account](https://blynk.cloud)
- Install **Blynk IoT App** for iOS or Android

## 1. Install our `MicroPython` build

Generic Dev Boards:

- `ESP32`: 4MB / 8MB / 16MB Flash (PSRAM is auto-detected)
- `ESP32-C3`: 4MB Flash
- `ESP32-S3`: 8MB Quad Flash, 8MB / 16MB Octa Flash (PSRAM is auto-detected)
- `Raspberry Pi Pico W`: 2MB Flash
- `Winner Micro W600`

Pre-configured devices:

- `Seeed EdgeBox-ESP-100`: WiFi + Ethernet + Cellular
- `TTGO T-Internet-COM`: WiFi + Ethernet + Cellular
- `TTGO T-PCIE`: WiFi + Cellular
- `TTGO T-Call SIM800C`: WiFi + Cellular/2G

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

There are many ways to program your device. We'll guide you through 2 most popular options:

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

---

## Further reading

- [Cookbook](_extra/Cookbook.md)
- [`asyncio` documentation](https://docs.micropython.org/en/latest/library/asyncio.html)
- [`asyncio` tutorial](https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md)

