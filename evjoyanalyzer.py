#!/usr/bin/python
import gamepad
from mainloop import MainLoop
import sys,time


class Program(MainLoop):
    def initialize(self):
        self.pad = gamepad.GamePad()

        self.pad.on_axischange += self.on_axischange
        self.pad.on_connect += self.on_connect
        self.pad.on_disconnect += self.on_disconnect
        self.pad.on_buttondown += self.on_buttondown
        self.pad.on_buttonup += self.on_buttonup

    def on_start(self):
        print("Waiting for gamepad...")
        self.pad.begin()

    def on_stop(self):
        print("\nStopping pad")
        self.pad.end()
        print("Stopped")

    def on_axischange(self,name,value):
        if value != 0:
            print("\nAxis '{0}' changed to {1}".format(name,value))
        
    def on_buttondown(self,name,value):
        print("\nButton '{0}' pressed".format(name)) 

    def on_buttonup(self,name,value):
        print("\nButton '{0}' released".format(name)) 

    def on_connect(self,padname):
        print("\nJoystick '{0}' connected".format(padname))

    def on_disconnect(self,padname):
        print("\nJoystick '{0}' disconnected".format(padname))

if __name__ == "__main__":
    Program().start()

