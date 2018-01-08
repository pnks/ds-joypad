import time
from event import Event
    

class MainLoop:
    def __init__(self):
        self._running = False
        self._events = {}
        self._eventqueue = []

        self._invokequeue = []

        self.initialize()

    def initialize(self):
        pass

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def start(self):
        if not self._running:
            self._running = True
            self._eventloop()

    def stop(self):
        if self._running:
            self._running = False


    def event(self,name):
        if not name in self._events:
            self._events[name] = Event()
        return self._events[name]

    def trigger(self,name,*args, **kwargs):
        self._eventqueue.append((name,args,kwargs))

    def invoke(self,c,*args, **kwargs):
        self._invokequeue.append((c,args,kwargs))

    def _eventloop(self):
        self.on_start()
        while self._running:
            # process all events
            for (name,args,kwargs) in self._eventqueue:
                self.event(name,*args,**kwargs)
                
            # process all invokes
            for (c,args,kwargs) in self._invokequeue:
                c(name,*args,**kwargs)

            #sleep 10ms
            time.sleep(0.010)
        self.on_stop()
