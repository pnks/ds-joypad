import gamepad
from mainloop import MainLoop
import sys,time

# grovepi init
PIN_RELAY = 2
PIN_CHAINLED = 3
NUM_CHAINLED = 1
PIN_LEDBAR = 4

import grovepi
grovepi.pinMode(PIN_RELAY,"OUTPUT");
grovepi.pinMode(PIN_CHAINLED,"OUTPUT");
grovepi.chainableRgbLed_init(PIN_CHAINLED, NUM_CHAINLED)

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
        if name == "SELECT":
            self.emstop = True
            print("Emergency Stop")
            PBR.SetMotor1(0)
            PBR.SetMotor2(0)
            print("Disabling Weapon")
            grovepi.digitalWrite(PIN_RELAY,0)
        elif name == "START":
            self.emstop = False
            print("Emergency Stop Released")
            
        if not self.emstop:
            if name == "TRI":
                print("Enabling Weapon")
                grovepi.digitalWrite(PIN_RELAY,1)            

    def on_buttonup(self,name,value):
        print("\nButton '{0}' released".format(name))
        if not self.emstop:
            if name == "TRI":
                print("Disabling Weapon")
                grovepi.digitalWrite(PIN_RELAY,0)

    def on_connect(self,padname):
        print("\nJoystick '{0}' connected".format(padname))

    def on_disconnect(self,padname):
        print("\nJoystick '{0}' disconnected".format(padname))

        print("Disabling motors")
        PBR.SetMotor1(0)
        PBR.SetMotor2(0)
        print("Disabling Weapon")
        grovepi.digitalWrite(PIN_RELAY,0)


if __name__ == "__main__":
    Program().start()

