#!/usr/bin/python

import gamepad
from mainloop import MainLoop
import sys,time


class Program(MainLoop):
    def initialize(self):
        self.pad = gamepad.DS3Controller()

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
        sys.stdout.write("\rX: {0:+03f}, Y: {1:+03f}, RX: {2:+03f}, RY: {3:+03f}, ACCROTZ: {4:+03f}"
                  .format(self.pad.axis("X"),
                          self.pad.axis("Y"),
                          self.pad.axis("RX"),
                          self.pad.axis("RY"),
                          self.pad.axis("ACCROTZ")))
        
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

