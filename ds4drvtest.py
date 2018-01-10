import gamepad
from mainloop import MainLoop
import sys,time

# grovepi init
PIN_RELAY = 2
PIN_CONNECTLED = 3

import grovepi
grovepi.pinMode(PIN_RELAY,"OUTPUT");
grovepi.pinMode(PIN_CONNECTLED,"OUTPUT");

# picoborg init
import PicoBorgRev
PBR = PicoBorgRev.PicoBorgRev()
PBR.Init()


class Program(MainLoop):
    def initialize(self):
        self.pad = gamepad.DS4Controller()

        self.emstop = False

        self.pad.on_axischange += self.on_axischange
        self.pad.on_connect += self.on_connect
        self.pad.on_disconnect += self.on_disconnect
        self.pad.on_buttondown += self.on_buttondown
        self.pad.on_buttonup += self.on_buttonup

        grovepi.digitalWrite(PIN_CONNECTLED,1)


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
        if name == "SHARE":
            self.emstop = True
            print("Emergency Stop")
            PBR.SetMotor1(0)
            PBR.SetMotor2(0)
            print("Disabling Weapon")
            grovepi.digitalWrite(PIN_RELAY,0)
        elif name == "OPTIONS":
            self.emstop = False
            print("Emergency Stop Released")
            
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
        grovepi.digitalWrite(PIN_CONNECTLED,0)


    def on_disconnect(self,padname):
        print("\nJoystick '{0}' disconnected".format(padname))
        grovepi.digitalWrite(PIN_CONNECTLED,1)

        print("Disabling motors")
        PBR.SetMotor1(0)
        PBR.SetMotor2(0)
        print("Disabling Weapon")
        grovepi.digitalWrite(PIN_RELAY,0)


if __name__ == "__main__":
    Program().start()

