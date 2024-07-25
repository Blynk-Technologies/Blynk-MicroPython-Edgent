
## 3. Modify the default example

Make sure your board is connected via USB. It should **not** be opened by any serial monitor.
Run these commands on your development machine:

```sh
# Install mpremote utility
pip3 install --upgrade mpremote

# Copy the example files to the device
mpremote cp main.py :
```

## 4. Run

Open MicroPython REPL:

```sh
mpremote repl
```

Press `Ctrl+D` to restart your app.

The device should get connected in a few seconds:

```log
      ___  __          __
     / _ )/ /_ _____  / /__
    / _  / / // / _ \/  '_/
   /____/_/\_, /_//_/_/\_\
          /___/

Connecting to WiFi_SSID... OK: 192.168.1.123
Connecting to MQTT broker...
Connected to Blynk.Cloud [secure]
```

## Edit System Config

You can edit `sysconfig` directly from MicroPython REPL:

```py
# Display all sysconfig
sysconfig

# Display parts of sysconfig
sysconfig.keys()
sysconfig['blynk']

# Disable watchdog (requires a hard reset)
sysconfig["wdt"]["enabled"] = False

# Enable color logs and set log level
sysconfig["log"].update({ "color": True, "level": "debug" })

# Remove network by index (0-based)
del sysconfig["nets"][2]

# Save settings
sysconfig.commit()
```

# Create OTA package

The `cfg/fw.json` will be used to identify the firmware version and type.
Firmware type should match the Blynk Template ID, unless:
- You have a single product that requires differant firmware upgrade packages
- You have multiple products that use a single firmware

```sh
python3 ./tools/mpota.py app_ota.tar.gz main.py cert/ca-bundle.pem `find ./lib -name '*.py'`
```

# Create recovery package

Create `cfg/sys.json` with your product details:
```json
{
  "blynk": {
    "tmpl_id": "TMPxxxxxxxx",
    "tmpl_name": "Device",
    "vendor": "Blynk",
    "server": "blynk.cloud"
  }
}
```

```sh
# Create recovery package
python3 ./tools/mpota.py recovery.tar.gz main.py cert/ca-bundle.pem cfg/sys.json

# Freeze into `_recovery` module
python3 ./tools/mkrecovery.py recovery.tar.gz > _recovery.py
```