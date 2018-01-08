Example code that uses evdev to read a DS3 gamepad. This could be used to have 
a DS3 controller control a robot. 

This code handles connecting and disconnecting your controller gracefully.


To use this code you need to install the python module evdev:

Use this command:

sudo pip install evdev



Also, you need to connect your DS3 (or after some updates DS4) controller to
your raspberry pi

For the DS3 controller, the instructions are as follows:
1. Reset the DS3 controller at the reset hole near L1
2. Prepare Bluetooth pairing
3. Connect the DS3 controller through USB
4. Press the PS button
5. Unplug the USB
6. Connect, and use 0000 as passcode

If the bluetooth pairing seems to fail, but the DS3 controllers shows a single
led at position 1, the connection might still be valid

To disconnect the controller, hold L1, R1 and PS button until the lights start blinking

