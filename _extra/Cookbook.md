
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
    "auth":      "rn60Wx*******",
    "server":    "blynk.cloud",
})

# Save system configuration
sysconfig.commit()
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

# Save system configuration
sysconfig.commit()
```

## Add diagnostics

```py
import netmgr
import micropython
import gc

async def diagnostics_task():
    while True:
        mem_prev = gc.mem_free()
        gc.collect()
        mem_free = gc.mem_free()
        gc.threshold(mem_free // 4 + gc.mem_alloc())
        edgent.publish("ds/Heap Free", mem_free / 1024)
        edgent.publish("ds/GC Collect", (mem_free - mem_prev) / 1024)
        edgent.publish("ds/WiFi RSSI", netmgr.sta.status("rssi"))
        await asyncio.sleep(60)
```

Also, add `diagnostics_task()` to `edgent.run_asyncio_loop`.

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
edgent.factory_reset()
```

## Update MicroPython firmware directly from GitHub (ESP32 only)

```py
from blynk import air
air.start_ota_update("https://micropython.org/resources/firmware/ESP32_GENERIC-SPIRAM-20240222-v1.22.2.app-bin", validate=False)
```
