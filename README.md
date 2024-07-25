
# Blynk.Edgent for MicroPython

Blynk offers custom MicroPython builds tailored for IoT applications.
These builds provide a standard, `asyncio`-based MicroPython environment enhanced with various fixes, improvements, and additional features:

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
  - OTA updates for MicroPython itself

# Getting Started

- Sign up/Log in to your [Blynk Account](https://blynk.cloud)
- Install **Blynk IoT App** for iOS or Android

## 1. Install `MicroPython` build from Blynk

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

## 2. Setup your board

Use **Blynk IoT App** to add the device to your account.
1. Open Blynk App
2. Click **Add device**
3. Select **Find devices nearby**
4. Select your device, follow the setup instructions

> [!NOTE]
> If you have already created your device in Blynk, you can skip the App-based provisioning and add your device by directly modifying the device configuration using REPL:
> ```py
> # Add WiFi network
> sysconfig["nets"].append({ "type": "wlan", "ssid": "YourSSID", "psk": "YourPassword" })
> 
> # Setup Blynk Template and Auth Token
> sysconfig["blynk"].update({
>     "tmpl_id":   "TMPxxxxxxxxxx",
>     "tmpl_name": "Device",
>     "auth":      "rn60Wx*******",
>     "server":    "blynk.cloud",
> })
> sysconfig.commit()
> ```
> When entering the production phase, you can **pre-configure** these settings and enable the **Factory Reset** function.

## 3. Edit the default firmware 

There are many ways to program your device. We'll guide you through 2 most popular options:

- [ViperIDE for Web and Mobile](_extra/Workflow-ViperIDE.md)
- [CLI using mpremote](_extra/Workflow-CLI.md)

---

## Further reading

- [`Blynk MQTT API documentation`](https://docs.blynk.io/en/blynk.cloud-mqtt-api/device-mqtt-api)
- [`asyncio` documentation](https://docs.micropython.org/en/latest/library/asyncio.html)
- [`asyncio` tutorial](https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md)
- [`mpremote` documentation](https://docs.micropython.org/en/latest/reference/mpremote.html)
- Alternative MQTT libraries like [mqtt_as](https://github.com/peterhinch/micropython-mqtt/tree/master/mqtt_as)

