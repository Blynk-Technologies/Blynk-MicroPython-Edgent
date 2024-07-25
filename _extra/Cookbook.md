
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
sysconfig.commit()
```

> [!NOTE]
> When entering the production phase, you can **pre-configure** these settings and enable the **Factory Reset** function.

## Change log level

```py
```

