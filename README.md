
# Blynk.Edgent for MicroPython

Blynk provides custom MicroPython builds specifically designed for IoT applications.
These builds offer a standard MicroPython environment, enriched with numerous fixes, improvements,
and additional features such as **Smartphone Apps, Web Dashboards, secure Blynk.Cloud connection, device claiming and provisioning, OTA updates, configuration storage**, [and more](#features).

![image](https://github.com/blynkkk/blynkkk.github.io/raw/master/images/GithubBanner.jpg?raw=1)

## Getting Started

- Sign up/Log in to your [Blynk Account](https://blynk.cloud)
- Install **Blynk IoT App** for [iOS](https://apps.apple.com/us/app/blynk-iot/id1559317868) or [Android](https://play.google.com/store/apps/details?id=cloud.blynk)

## 1. Install MicroPython + Blynk.Edgent

<details>
  <summary>See instructions for <b>ESP32</b> based devices</summary></br>

You can use [**ESP Launchpad**](https://espressif.github.io/esp-launchpad/?flashConfigURL=https://blynk-fw-builds.fra1.cdn.digitaloceanspaces.com/Blynk-Edgent-MicroPython/latest/esp-quickstart.toml) to flash your device. You will need a Chrome-based browser.

1. Plug your board into a USB port
2. Click <kbd>Connect</kbd> in upper right corner and select your board
   - Recommended: click <kbd>Erase Flash</kbd> on the **DIY** tab
4. Select **Application** (generic boards vs specialized builds)
5. Select **Develop Kit** variant based on flash size and type
6. Click the <kbd>Flash</kbd> button (if disabled, try clicking the `Connect` button again)
7. Press <kbd>Reset</kbd> button on your board to run the MicroPython firmware

> Alternatively, you can [flash your ESP32 device manually](https://github.com/Blynk-Technologies/Blynk-MicroPython-Edgent/releases/latest)

</details>

<details>
  <summary>See instructions for <b>Raspberry Pi Pico W</b></summary></br>

1. Hold down the <kbd>BOOTSEL</kbd> button while plugging the board into a USB port
2. Copy the latest [UF2 firmware file](https://blynk-fw-builds.fra1.cdn.digitaloceanspaces.com/Blynk-Edgent-MicroPython/latest/RPI_PICO_W.uf2) to the USB mass storage device that appears
3. Once programming of the new firmware is complete, the device will automatically reset and be ready for use

</details>

## 2. Connect your device to Blynk.Cloud

> [!WARNING]
> The automatic connection using Blynk Apps is currently in development.  
> For now please [connect your device manually using REPL](_extra/Cookbook.md#manual-device-connection)

<!--
1. Open **Blynk IoT App** on your smartphone
2. Click **Add device** -> **Find devices nearby**
3. Select your device and follow the setup instructions

> [!NOTE]
> If you have already created your device in Blynk,
> you can [connect it manually using REPL](_extra/Cookbook.md#manual-device-connection)
-->

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
- `netmgr` - Automatic network management
  - `WiFi`: Maintains connection to the most reliable WiFi network (up to 16 configured networks)
  - `Ethernet`: Supports `Static IP` or `DHCP` network configuration
  - `Cellular`: Provides connectivity through `2G GSM`, `EDGE`, `3G`, `4G LTE`, `Cat M1`, or `5G` networks using `PPP`
- `config` - System-wide configuration registry
- `aiontp` - A versatile asyncio-based `NTP` client
- `aiohttp` - Asyncio-based `HTTP v1.1` client with session `keep-alive` support
- `aiomqtt` - Asyncio-based `MQTT v3.1.1` client
- `aioinput` - An asyncio variant of `input` function
- `aioprof` - Asyncio [profiling tool](https://gitlab.com/alelec/aioprof)
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
