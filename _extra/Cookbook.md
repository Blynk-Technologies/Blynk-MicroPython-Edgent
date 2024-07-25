
# MicroPython + Blynk.Edgent Cookbook

## Manual device connection

Connect your device to Blynk.Cloud by directly modifying the device configuration using REPL:

```py
# Add WiFi network
sysconfig["nets"].append({ "type": "wlan", "ssid": "YourSSID", "psk": "YourPassword" })

# Setup Blynk Template and Auth Token
sysconfig["blynk"].update({
    "tmpl_id":   "TMPxxxxxxxxxx",
    "tmpl_name": "Device",
    "auth":      "rn60Wx*******",
    "server":    "blynk.cloud",
})

# Save device configuration
sysconfig.commit()
```

> [!NOTE]
> When entering the production phase, you can **pre-configure** these settings and enable the **Factory Reset** function. Please contact Blynk for guidance.

## Change logger settings

```py
sysconfig["log"].update({ "color": True, "level": "debug" })
sysconfig.commit()
machine.reset()
```

## Watchdog Timer

Most of builds come with the watchdog disabled by default.

```py
sysconfig["wdt"]["enabled"] = True     # or False
sysconfig.commit()
machine.reset()
```

## Format internal FS

> [!WARNING]
> This performs a factory reset, the internal file system will recover to it's initial state

Use one of these commands depending on your actual hardware:
```py
# ESP32
import os, flashbdev; os.VfsLfs2.mkfs(flashbdev.bdev)

# RP2040
import vfs, rp2; vfs.VfsLfs2.mkfs(rp2.Flash(), progsize=256)

# WM W600
import vfs, w600; vfs.VfsLfs2.mkfs(w600.Flash(), progsize=256)
```

## Update MicroPython firmware directly from GitHub (ESP32 only)

```py
blynk.air.start_ota_update("https://micropython.org/resources/firmware/ESP32_GENERIC-SPIRAM-20240222-v1.22.2.app-bin", validate=False)
```
