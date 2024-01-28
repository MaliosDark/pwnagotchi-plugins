
## Educational-purposes-exclusively
This plugin is designed for educational purposes, enabling automatic authentication to known networks and performing internal network reconnaissance. Please be aware of the following considerations before using this experimental plugin.

 **Inspired on the Educational Purposes Only Plugin [GitHub Repository](https://github.com/c-nagy/pwnagotchi-educational-purposes-only-plugin)**

### Dangers of Using This Plugin

1. **Experimental Nature:** This plugin is experimental and may have unforeseen issues. It is recommended to use it in a controlled environment.

2. **Hidden Messages Bug:** There is a known bug where main messages are hidden upon starting the plugin. It's unclear if the plugin is executing correctly. Please take note of this behavior.

### TODOs

- [ ] Investigate the bug causing the hiding of main messages upon plugin initiation.
- [ ] Implement a status indicator to confirm the proper execution of the plugin.

## Usage

1. Ensure you are in a controlled educational environment.
2. Use the plugin responsibly and avoid deploying it in production scenarios.
3. Keep an eye on the plugin's status indicators for any unexpected behavior.

   

### Installation of Other Plugins

#### Experience Plugin [GitHub Repository](https://github.com/GaelicThunder/Experience-Plugin-Pwnagotchi)

To enable the Experience Plugin, modify the configuration file as follows:

```ini
main.plugins.exp.enabled = true
main.plugins.exp.lvl_x_coord = 0
main.plugins.exp.lvl_y_coord = 81
main.plugins.exp.exp_x_coord = 38
main.plugins.exp.exp_y_coord = 81
main.plugins.exp.bar_symbols_count = 12
```

#### Age Plugin [GitHub Repository](https://github.com/hannadiamond/pwnagotchi-plugins)

To enable the Age Plugin, modify the configuration file as follows:

```ini
main.plugins.age.enabled = true
main.plugins.age.age_x_coord = 0
main.plugins.age.age_y_coord = 32
main.plugins.age.str_x_coord = 67
main.plugins.age.str_y_coord = 32
```

Make sure to adjust the coordinates and settings according to your preferences and requirements.

### Configuration Settings

Add the following configuration settings to your main configuration file:

```ini
main.plugins.educational-purposes-exclusively.home-network = "SSID-HOME"
main.plugins.educational-purposes-exclusively.home-password = "password"
main.plugins.educational-purposes-exclusively.enabled = true
```

Adjust the values for `home-network` and `home-password` according to your network credentials. Ensure that the plugin is enabled by setting `enabled` to `true`.

## How to Contribute

Feel free to contribute by addressing the TODOs, reporting bugs, or proposing improvements. Pull requests are welcome!
