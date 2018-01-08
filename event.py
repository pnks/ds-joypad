# License for this source file
# 
# Copyright (c) 2014 KHPhone team
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE


'''
Provides generic event object that allows callback registration to events. 

'''

class Event(object):
    '''
    Generic event object providing callback registration.
    
    Event listeners are callables.
    The semantics of the argument list to the callbacks is not hardcoded in this class;
    instead is it implied by the context where this Event object lives.
    Registration and unregistration are done by the += and -= operators.
    A callable can only be registered once and only be unregistered once.
    The event is fired by calling the event object itself with the desired parameters.    
    
    Example:
    
        >>> def listener(message):
        ...    print message;
        >>> event = Event();
        >>> event("x");
        >>> event += listener;
        >>> event("x");
        x
        >>> event -= listener;
        >>> event("x");

    '''
    def __init__(self):
        self.listeners = [];
    def __iadd__(self, listener):
        """
        Add new event listener.
        @param listener: callable; will be called whenever the event fires.
        @return: self.
        @raise ValueError: if the listener has already been registered for this event. 
        """
        if listener in self.listeners:
            raise ValueError("Listener already registered to event");
        self.listeners.append(listener);
        return self;
    def __isub__(self, listener):
        """
        Remove previously registered event listener.
        @param listener: previously registered event listener.
        @return: self.
        @raise ValueError: if the listener is not registered for this event.
        """
        if listener not in self.listeners:
            raise ValueError("Listener not registered to event");
        self.listeners.remove(listener);
        return self;
    def __call__(self, *args, **kwargs):
        """
        Fire event, passing the specified arguments to all listeners.
        Each listener will be called with listener(*args, **kwargs).
        """
        for listener in list(self.listeners):
            listener(*args, **kwargs);
