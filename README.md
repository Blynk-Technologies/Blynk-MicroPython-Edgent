
# Blynk.Edgent for MicroPython

Blynk provides custom MicroPython builds specifically designed for IoT applications.
These builds offer a standard MicroPython environment, enriched with numerous fixes, improvements,
and additional features such as **secure Blynk.Cloud connection, device claiming and provisioning, OTA updates, configuration storage**, [and more](#features).

## Getting Started

- Sign up/Log in to your [Blynk Account](https://blynk.cloud)
- Install **Blynk IoT App** for iOS or Android

## 1. Install our `MicroPython` build

<details>
  <summary>See instructions for <b>ESP32, ESP32-S3, ESP32-C3</b> based devices</summary></br>

You can use [**ESP Launchpad**](https://espressif.github.io/esp-launchpad/?flashConfigURL=https://vsh.pp.ua/Blynk-MicroPython-Edgent/esp-quickstart.toml) to flash your device. You will need a Chrome-based browser.

1. Plug your board into a USB port
2. Click `Connect` in upper right corner and select your board
3. Select **Application** (generic boards vs specialized builds)
4. Select **Develop Kit** variant based on flash size and type
5. Click the `Flash` button (if disabled, try clicking the `Connect` button again)
6. Press `Reset` button on your board to run the MicroPython firmware

> Alternatively, you can [flash your ESP32 device manually](https://github.com/Blynk-Technologies/Blynk-MicroPython-Edgent/releases/latest)

</details>

<details>
  <summary>See instructions for <b>Raspberry Pi Pico W</b></summary></br>

1. Hold down the `BOOTSEL` button while plugging the board into a USB port
2. Copy the latest `UF2 firmware file` to the USB mass storage device that appears
3. Once programming of the new firmware is complete, the device will automatically reset and be ready for use

</details>

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
        edgent.publish("Uptime", ticks_ms())

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
