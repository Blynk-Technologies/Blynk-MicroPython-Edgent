## Using `ViperIDE`

Make sure your board is connected via USB. It should **not** be opened by any serial monitor or other tool.  
Open [ViperIDE](https://viper-ide.org) (you'll need a Chrome-based browser).

[<img src="https://github.com/vshymanskyy/ViperIDE/blob/main/docs/images/visual-main.png?raw=1" alt="image" style="width:50%;"/>](https://viper-ide.org)

1. In the upper right corner, click `USB` button
2. Select your port
3. The device should get connected

> [!NOTE]
> When ViperIDE connects to the device via USB, the `asyncio` loop is stopped.  
> You'll need to click the <kbd>Soft Reset</kbd> button to restart your main App

---

# Further reading

- [ViperIDE tips and tricks](https://github.com/vshymanskyy/ViperIDE/tree/main/docs)
- [Blynk.Edgent Cookbook](Cookbook.md)

