
# MicroPython + Blynk.Edgent Cookbook

## Manual device connection

Connect your device to Blynk.Cloud by directly modifying the device configuration using REPL:

```py
# Add your WiFi network
sysconfig["nets"].append({ "type": "wlan", "ssid": "YourSSID", "psk": "YourPassword" })

# Setup Blynk Template and Auth Token
sysconfig["blynk"].update({
    "tmpl_id":   "TMPxxxxxxxxxx",
    "tmpl_name": "Device",
    "auth":      "rn60Wxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "server":    "blynk.cloud",
})

# Save system configuration
sysconfig.commit()

# Restart
import machine
machine.reset()
```

> [!NOTE]
> When entering the production phase, you can **pre-configure** these settings and enable the **Factory Reset** function. Please contact Blynk for guidance.

## Edit System Config

You can edit `sysconfig` directly from MicroPython REPL:

```py
# Display complete sysconfig
sysconfig

# Display parts of sysconfig
sysconfig.keys()
sysconfig['blynk']

# Enable color logs and set log level
sysconfig["log"].update({ "color": True, "level": "debug" })

# Add your WiFi network
sysconfig["nets"].append({ "type": "wlan", "ssid": "YourSSID", "psk": "YourPassword" })

# Remove network by index (0-based)
del sysconfig["nets"][2]

# Remove all networks
sysconfig['nets'].clear()

# Save system configuration
sysconfig.commit()
```

## Add your connectivity options

If your board has additional connectivity options like `Etheret` or `Cellular`, you can add them to `board.py`.
Please [see examples](./boards).  
You can override the built-in `board` module by placing your variant in `lib/board.py`:
```sh
mpremote cp _extra/boards/ttgo-t-internet-com.py :lib/board.py
```
After rebooting the device, the `netmgr` should be able to detect the new board definitions.

## Add diagnostics

```py
import netmgr
import gc

async def diagnostics_task():
    while True:
        mem_prev = gc.mem_free()
        gc.collect()
        mem_free = gc.mem_free()
        gc.threshold(mem_free // 4 + gc.mem_alloc())
        edgent.publish("Heap Free", mem_free / 1024)
        edgent.publish("GC Collect", (mem_free - mem_prev) / 1024)
        edgent.publish("WiFi RSSI", netmgr.sta.status("rssi"))
        await asyncio.sleep(60)
```

Also, add `diagnostics_task()` to `edgent.run_asyncio_loop`.

## BLE-assisted provisioning

TODO

## Remote MicroPyhton REPL

TODO

## Local Time and Timezone

TODO

## Sunrise/Sunset

TODO

## OTA update of MicroPython filesystem

TODO

## OTA update of MicroPython system directly from URL (ESP32 only)

First, let's define the URL where our MicroPython firmware ota package is hosted:
```py
base_url = "https://blynk-fw-builds.fra1.cdn.digitaloceanspaces.com"
fw_url = base_url + "/Blynk-Edgent-MicroPython/v0.3.0/GENERIC_ESP32_4MB.ota.bin"
```

How to launch the OTA process depends on the context.

#### Blynk terminal Widget

```py
import blynk.air
blynk.air.start_ota_update(fw_url, validate=False)
```

#### Serial REPL

```py
import blynk.air, asyncio
blynk.air.start_ota_update(fw_url, validate=False)
asyncio.run_until_complete()
```

You should see the firmware download progress:

```log
1101994 I blynk.air    Downloading update
1120261 D blynk.air    Complete: 10%
1137007 D blynk.air    Complete: 20%
1153807 D blynk.air    Complete: 30%
1170321 D blynk.air    Complete: 40%
...
```

## Watchdog Timer (WDT)

The watchdog is typically disabled by default, as it can complicate prototyping.
It is recommended to enable it at later stages of development:

```py
sysconfig["wdt"]["enabled"] = True
sysconfig.commit()
machine.reset()      # Changing this setting requires a hard reset
```

## Format internal FS

> [!WARNING]
> This performs a factory reset, the internal file system will recover to it's initial state

```py
from blynk import edgent
edgent.factory_reset()
```
