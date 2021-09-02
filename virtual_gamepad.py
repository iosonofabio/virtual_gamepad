""" rpi-gpio-jstk.py by Chris Swan 9 Aug 2012
GPIO Joystick driver for Raspberry Pi for use with 80s 5 switch joysticks
based on python-uinput/examples/joystick.py by tuomasjjrasanen
https://github.com/tuomasjjrasanen/python-uinput/blob/master/examples/joystick.py
requires uinput kernel module (sudo modprobe uinput)
requires python-uinput (git clone https://github.com/tuomasjjrasanen/python-uinput)
requires python RPi.GPIO (from http://pypi.python.org/pypi/RPi.GPIO/0.3.1a)
for detailed usage see http://blog.thestateofme.com/2012/08/10/raspberry-pi-gpio-joystick/
Changes
19 Aug 2012 - inputs set to use internal pull ups rather than external 10k resistors
"""

from collections import defaultdict
import pynput
import uinput
import time

events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_TL,
    uinput.BTN_TR,
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    uinput.ABS_X + (0, 255, 0, 0),
    uinput.ABS_Y + (0, 255, 0, 0),
)
device = uinput.Device(
    events,
    vendor=0x045e,
    product=0x028e,
    version=0x110,
    name="Microsoft X-Box 360 pad",
)

# Center joystick
# syn=False to emit an "atomic" (128, 128) event.
device.emit(uinput.ABS_X, 128, syn=False)
device.emit(uinput.ABS_Y, 128)

keymap = {
    'right': 'l',
    'left': 'j',
    'up': 'i',
    'down': 'k',
    'jump': '[',
    'action': ']',
    'inventory': '=',
    'confirm': '0',
    '?': '-',
    'requests/cancel': '9',
    'zoomout': '8',
    'back': 'p',
}
keys = list(keymap.values())

def find_key(key):
    #if key == keyboard.Key.esc:
    #    return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k not in keys:
        return True

    return k

    #print('Key pressed: ' + k)
    #return False  # stop listener; remove this if want more keys 


def on_press(key):
    k = find_key(key)
    if k is True:
        return True

    if k == keymap['jump']:
        device.emit(uinput.BTN_A, 1)
    elif k == keymap['back']:
        device.emit(uinput.BTN_B, 1)
    elif k == keymap['action']:
        device.emit(uinput.BTN_X, 1)
    elif k == keymap['inventory']:
        device.emit(uinput.BTN_Y, 1)
    elif k == keymap['confirm']:
        device.emit(uinput.BTN_TL, 1)
    elif k == keymap['?']:
        device.emit(uinput.BTN_TR, 1)
    elif k == keymap['requests/cancel']:
        device.emit(uinput.BTN_THUMBL, 1)
    elif k == keymap['zoomout']:
        device.emit(uinput.BTN_THUMBR, 1)
    elif k == keymap['up']:
        device.emit(uinput.ABS_Y, 0)                    # Zero Y
    elif k == keymap['down']:
        device.emit(uinput.ABS_Y, 255)                  # Max Y
    elif k == keymap['left']:
        device.emit(uinput.ABS_X, 0)                    # Zero X
    elif k == keymap['right']:
        device.emit(uinput.ABS_X, 255)                  # Max X

    return True


def on_release(key):
    k = find_key(key)
    if k is True:
        return True

    if k == keymap['jump']:
        device.emit(uinput.BTN_A, 0)
    elif k == keymap['back']:
        device.emit(uinput.BTN_B, 0)
    elif k == keymap['action']:
        device.emit(uinput.BTN_X, 0)
    elif k == keymap['inventory']:
        device.emit(uinput.BTN_Y, 0)
    elif k == keymap['confirm']:
        device.emit(uinput.BTN_TL, 0)
    elif k == keymap['?']:
        device.emit(uinput.BTN_TR, 0)
    elif k == keymap['requests/cancel']:
        device.emit(uinput.BTN_THUMBL, 0)
    elif k == keymap['zoomout']:
        device.emit(uinput.BTN_THUMBR, 0)
    elif k == keymap['up']:
        device.emit(uinput.ABS_Y, 128)                # Center Y
    elif k == keymap['down']:
        device.emit(uinput.ABS_Y, 128)                # Center Y
    elif k == keymap['left']:
        device.emit(uinput.ABS_X, 128)                # Center Y
    elif k == keymap['right']:
        device.emit(uinput.ABS_X, 128)                # Center Y

    #time.sleep(.02)    # Poll every 20ms (otherwise CPU load gets too high)

    return True


if True:
    listener = pynput.keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        )
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys
