
# Using `mpremote`

Make sure your board is connected via USB. It should **not** be opened by any serial monitor or other tool.
Run these commands on your development machine:

```sh
# Install mpremote utility
pip3 install --upgrade mpremote

# Copy the example files to the device
mpremote cp main.py :
```

> [!NOTE]
> If you have any issues with this, please check out the [`mpremote` documentation](https://docs.micropython.org/en/latest/reference/mpremote.html)

Then, open MicroPython REPL:

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

# Create OTA package

The `cfg/fw.json` will be used to identify the firmware version and type.
Firmware type should match the Blynk Template ID, unless:
- You have a single product that requires differant firmware upgrade packages
- You have multiple products that use a single firmware

```sh
python3 ./tools/mpota.py app_ota.tar.gz main.py cert/ca-bundle.pem `find ./lib -name '*.py'`
```

