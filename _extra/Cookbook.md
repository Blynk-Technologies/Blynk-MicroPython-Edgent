
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
> When entering the production phase, you can **pre-configure** these settings and enable the **Factory Reset** function.

## Change logger settings

```py
sysconfig["log"].update({ "color": True, "level": "debug" })
```

## Watchdog Timer

```py
sysconfig["wdt"]["enabled"] = False
```

## Format internal FS

Use one of these commands depending on your actual hardware:
```py
# ESP32
import os, flashbdev; os.VfsLfs2.mkfs(flashbdev.bdev)

# RP2040
import vfs, rp2; vfs.VfsLfs2.mkfs(rp2.Flash(), progsize=256)

# WM W600
import vfs, w600; vfs.VfsLfs2.mkfs(w600.Flash(), progsize=256)
```
