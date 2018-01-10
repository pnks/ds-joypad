from evdev import InputDevice, categorize, ecodes
from event import Event
import time, sys
import threading


class ItemCollection:
    def __init__(self):
        self.items = []

    def byName(self,name):
        for item in self.items:
            if item.name == name:
                return item
        raise LookupError("Could not find item for name {0}".format(name))

            
    def byCode(self,code):
        for item in self.items:
            if item.code == code:
                return item
        raise LookupError("Could not find item for code {0}".format(code))

    def __len__(self):
        return len(self.items)

    def __getitem__(self,key):
        return self.items[key]

    def __iter__(self):
        return iter(self.items)

    def __reversed__(self):
        return reversed(self.items)


class Axis:
    def __init__(self,code,name, minraw = 0,maxraw = 255,deadzone=0.1,default=0):
        self.code = code
        self.name = name
        self.minraw = minraw
        self.maxraw = maxraw
        self.deadzone = deadzone
        self.value = default

    def setRaw(self, raw):
        rawrange = self.maxraw - self.minraw
        self.value = (2*(1.0*raw - self.minraw) - rawrange)/ (rawrange)

        # apply deadzone
        if abs(self.value) < self.deadzone:
            self.value = 0

class Axes(ItemCollection) :
    def register(self,code,name,minraw = 0, maxraw = 255, deadzone=0.1, default=0):
        self.items.append(Axis(code,name,minraw,maxraw,deadzone,default))
    

class Button:
    def __init__(self,code, name):
        self.code = code
        self.value = False
        self.name = name


class Buttons(ItemCollection):
    def register(self,code,name):
        self.items.append(Button(code,name))


class GamePad:
    def __init__(self,address='/dev/input/event0'):
        self._file = address

        self._loop_running = False

        self.joypadconnected = False
        self.joypadName = None
        self.axes = Axes()        
        self.buttons = Buttons()

        self.initialize()
        
        self.on_connect = Event()
        self.on_disconnect = Event()
        self.on_buttondown =  Event()
        self.on_buttonup =  Event()
        self.on_axischange = Event()

        self.thread = threading.Thread(None, self._eventloop)

    def initialize(self):
        pass

    def begin(self):
        if not self.thread.is_alive():
            self._loop_running = True
            self.thread.run()

    def end(self):
        if self.thread.is_alive():
            self._loop_running = False
            thread.join()

    def __del__(self):
        self.end()

    def _eventloop(self):
        connected = False
        while self._loop_running:
            try:
                if not connected:
                    # attempt to (re) connect to the joystick/joypad
                    self.gamepad = InputDevice(self._file)
                    connected = True
                    self.joypadconnected = True
                    self.on_connect(self.gamepad.name)
                
                for event in self.gamepad.read_loop():
                    self._processEvent(event)

            except (IOError, OSError) as x:
                if connected:
                    connected = False
                    self.joypadconnected = False
                    self.on_disconnect(self.gamepad.name)
                    
                time.sleep(0.25) # sleep 250 ms
                # try connecting again next pass
            
            pass
        
    def _processEvent(self,event):
        if event.type == ecodes.EV_KEY:

            try:
                button = self.buttons.byCode(event.code)
            except LookupError:
                print("Could not find button for code {0}, ad hoc registered as BTN_{0}".format(event.code))
                self.buttons.register(event.code,"BTN_{0}".format(event.code))
                button = self.buttons.byCode(event.code)

            button.value = True if event.value else False
            if button.value:
                self.on_buttondown(button.name,button.value)
            else:
                self.on_buttonup(button.name,button.value)
            
        elif event.type == ecodes.EV_ABS:
            try:
                axis = self.axes.byCode(event.code)
            except LookupError:
                print("Could not finf axis for code {0}, ad hoc registered as AXIS_{0}".format(event.code))
                self.axes.register(event.code,"AXIS_{0}".format(event.code),0,255)
                axis = self.axes.byCode(event.code)
                
            axis.setRaw(event.value)
            self.on_axischange(axis.name,axis.value)

    def list_buttons(self):
        l = []
        for btn in self.buttons:
            l.append(btn.name)
        return l

    def list_axes(self):
        l = []
        for axis in self.axes:
            l.append(axis.name)
        return l

    def button(self,name):
        button = self.buttons.byName(name)
        return button.value if button is not None else None

    def axis(self,name):
        axis = self.axes.byName(name)
        return axis.value if axis is not None else None

    

class DS3Controller(GamePad):
    def initialize(self):
        self.buttons.register(302, "X")
        self.buttons.register(301, "O")
        self.buttons.register(303, "SQR")
        self.buttons.register(300, "TRI")
        self.buttons.register(291, "START")
        self.buttons.register(288, "SELECT")
        self.buttons.register(298, "L1")
        self.buttons.register(299, "R1")
        self.buttons.register(296, "L2")
        self.buttons.register(297, "R2")
        self.buttons.register(292, "UP")
        self.buttons.register(294, "DOWN")
        self.buttons.register(295, "LEFT")
        self.buttons.register(293, "RIGHT")
        self.buttons.register(289, "LS")
        self.buttons.register(290, "RS")
        self.buttons.register(704, "HOME")
            
        self.axes.register( 0,"X",0,255)
        self.axes.register( 1,"Y",255,0)
        self.axes.register( 2,"RX",0,255)
        self.axes.register( 5,"RY",255,0)
        self.axes.register(44,"UP",0,255)
        self.axes.register(45,"RIGHT",0,255)
        self.axes.register(46,"DOWN",0,255)
        self.axes.register(47,"LEFT",0,255)
        self.axes.register(48,"L2",0,255)
        self.axes.register(49,"R2",0,255)
        self.axes.register(50,"L1",0,255)
        self.axes.register(51,"R1",0,255)
        self.axes.register(52,"BTTRI",0,255)
        self.axes.register(53,"BTO",0,255)
        self.axes.register(54,"BTX",0,255)
        self.axes.register(55,"BTSQR",0,255)
            
        self.axes.register(59,"ACCX",0,1024)
        self.axes.register(60,"ACCY",0,1024)
        self.axes.register(61,"ACCZ",0,1024)
        self.axes.register(62,"ACCROTZ",0,1024)

class DS4Controller(GamePad):
    def initialize(self):
        self.buttons.register(304, "SQR")
        self.buttons.register(305, "X")
        self.buttons.register(306, "O")
        self.buttons.register(307, "TRI")
        self.buttons.register(308, "L1")
        self.buttons.register(309, "R1")
        self.buttons.register(310, "L2")
        self.buttons.register(311, "R2")
        self.buttons.register(312, "SHARE")
        self.buttons.register(313, "OPTIONS")

        self.buttons.register(314, "LS")
        self.buttons.register(315, "RS")
        self.buttons.register(316, "HOME")
        self.buttons.register(317, "PANEL")
            
        self.axes.register( 0,"X",0,255)
        self.axes.register( 1,"Y",255,0)
        self.axes.register( 2,"RX",0,255)
        self.axes.register( 3,"L2",0,255,default=-1.0)
        self.axes.register( 4,"R2",0,255,default=-1.0)
        self.axes.register( 5,"RY",255,0)
        
        self.axes.register(16,"HATX",0,255)
        self.axes.register(17,"HATY",0,255)

 
