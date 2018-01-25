#!/usr/bin/python
import gamepad
from mainloop import MainLoop
import sys,time,os

# grovepi init
PIN_RELAY = 4
PIN_CLED = 2

import grovepi
grovepi.pinMode(PIN_RELAY,"OUTPUT");
grovepi.pinMode(PIN_CLED,"OUTPUT")
grovepi.chainableRgbLed_init(PIN_CLED, 1)

def setColor(r,g,b):
    grovepi.storeColor(r,g,b)
    time.sleep(.1)
    grovepi.chainableRgbLed_pattern(PIN_CLED,0, 0)

# picoborg init
import PicoBorgRev
PBR = PicoBorgRev.PicoBorgRev()
PBR.Init()


class Program(MainLoop):
    def initialize(self):
        self.pad = gamepad.DS3Controller()

        self.emstop = False

        self.pad.on_axischange += self.on_axischange
        self.pad.on_connect += self.on_connect
        self.pad.on_disconnect += self.on_disconnect
        self.pad.on_buttondown += self.on_buttondown
        self.pad.on_buttonup += self.on_buttonup

    def on_start(self):
        print("Waiting for gamepad...")
        setColor(0,0,255)
        self.pad.begin()

    def on_stop(self):
        print("\nStopping pad")
        self.pad.end()
        print("Stopped")

    def on_axischange(self,name,value):
        x = self.pad.axis("X")
        y = self.pad.axis("Y")

        a = y - x
        b = y + x

        if not self.emstop:
            PBR.SetMotor1(a)
            PBR.SetMotor2(-b)
        
    def on_buttondown(self,name,value):
        print("\nButton '{0}' pressed".format(name))
        if name == "UP":
            self.emstop = True
            setColor(255,255,0)

            print("Emergency Stop")
            PBR.SetMotor1(0)
            PBR.SetMotor2(0)
            print("Disabling Weapon")
            grovepi.digitalWrite(PIN_RELAY,0)
        elif name == "DOWN":
            setColor(0,255,0)
            self.emstop = False
            print("Emergency Stop Released")
        elif name == "START":
            os.system("sudo halt")
            
        if not self.emstop:
            if name == "TRI":
                print("Enabling Weapon")
                grovepi.digitalWrite(PIN_RELAY,1)            
            elif name == "O":
                print("Disabling Weapon")
                grovepi.digitalWrite(PIN_RELAY,0)

    def on_buttonup(self,name,value):
        print("\nButton '{0}' released".format(name))
            
    def on_connect(self,padname):
        print("\nJoystick '{0}' connected".format(padname))
        setColor(0,255,0)


    def on_disconnect(self,padname):
        print("\nJoystick '{0}' disconnected".format(padname))
        setColor(0,0,255)

        print("Disabling motors")
        PBR.SetMotor1(0)
        PBR.SetMotor2(0)
        print("Disabling Weapon")
        grovepi.digitalWrite(PIN_RELAY,0)


if __name__ == "__main__":
    Program().start()

