class Axis:
    def __init__(self,code,name, minraw = 0,maxraw = 255):
        self.code = code
        self.name = name,
        self.minraw = minraw
        self.maxraw = maxraw;
        self.value = 0

    def setRaw(self, raw):
        rawrange = self.maxraw - self.minraw
        self.value = (2*(1.0*raw - self.minraw) - rawrange)/ (rawrange)

class Axes:
    def __init__(self):
        self.axes = []

    def register(self,code,name,minraw = 0, maxraw = 255):
        self.axes.append(Axis(code,name,minraw,maxraw))

    def byName(self,name):
        for axis in self.axes:
            if axis.name == name:
                return axis
        return None
            
    def byCode(self,code):
        for axis in self.axes:
            if axis.code == code:
                return axis
        return None

    def __len__(self):
        return len(self.axes)

    def __getitem__(self,key):
        return self.axes[key]

    def __iter__(self):
        return iter(self.axes)

    def __reversed__(self)
        return reversed(self.axes)
    
