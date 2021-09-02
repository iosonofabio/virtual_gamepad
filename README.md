 [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
## Virtual gamepad in Linux
Inspiration and some code from:
 
- https://github.com/tuomasjjrasanen/python-uinput/blob/master/examples/joystick.py
- http://blog.thestateofme.com/2012/08/10/raspberry-pi-gpio-joystick/
- https://github.com/ynsta/steamcontroller

### How to use:
(Install and) Load the `uinput` module:
```bash
sudo modprobe uinput
```
Run the script:
```bash
python virtual_gamepad.py
```
(run your game or software requiring a gamepad...)

After your software is closed again, stop the script if you don't need the gamepad anymore.

**NOTE**: whoever runs the script must have access to /dev/uinput. You can either run it as root/sudo, or give your user priviledges via a group, e.g.
```bash
sudo groupadd uinput
sudo usermod -aG uinput "$USER"
sudo chmod g+rw /dev/uinput
sudo chgrp uinput /dev/uinput
```
after which you won't need sudo to launch the virtual gamepad anymore.

### Technicalities
- The script emulates an Xbox controller.
- Take a look at the script to bind the keys differently.
- The third repo link above has more keys, haptics, and more. Add them as needed.
