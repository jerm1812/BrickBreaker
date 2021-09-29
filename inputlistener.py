#inputlistener.py
"""Library to add basic event capabilities to the graphics.py library provided by John Zelle

This is the testing release for my students only, created by Jeremy Porier on November 13, 2014
"""

__version__ = "0.1"

from graphics import Point

class InputListener:

    def __init__(self, graphwin):
        self._alarmID = None
        self._keyPressHandler = None
        self._keyReleaseHandler = None
        self._mouseMoveHandler = None
        self._mouseClickHandler = None
        self._graphwin = graphwin
        graphwin.bind_all('<KeyPress>', self._keypress)
        graphwin.bind_all('<KeyRelease>',self._eachkeyrelease)
        graphwin.bind('<Motion>',self._mousemove)
        graphwin.bind_all('<Button-1>',self._mouseclick)

    def _keypress(self, key):
        #processes KeyPress events and eliminates repetition if the button is held down
        if self._keyPressHandler is not None:
            if self._alarmID is None:
                self._keyPressHandler(key.keysym)
            else:
                self._graphwin.after_cancel(self._alarmID)
                self._alarmID = None

    def _keyrelease(self, key):
        #used to compensate for the repetition of KeyRelease events when a button is held down
        if self._keyReleaseHandler is not None:
            self._keyReleaseHandler(key.keysym)
        self._alarmID = None

    def _eachkeyrelease(self, key):
        #processes each individual key release event
        newAlarmID = self._graphwin.after_idle(self._keyrelease, key)
        self._alarmID = newAlarmID

    def _mousemove(self, position):
        if self._mouseMoveHandler is not None:
            #sends a Point object to the handler
            self._mouseMoveHandler(Point(position.x,position.y))

    def _mouseclick(self, position):
        if self._mouseClickHandler is not None:
            #sends a Point object to the handler
            self._mouseClickHandler(Point(position.x,position.y))

    def setKeyPressHandler(self, handler):
        self._keyPressHandler = handler

    def setKeyReleaseHandler(self, handler):
        self._keyReleaseHandler = handler

    def setMouseMoveHandler(self, handler):
        self._mouseMoveHandler = handler

    def setMouseClickHandler(self, handler):
        self._mouseClickHandler = handler
        
        
    
