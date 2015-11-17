# Animation.py

import random
from Tkinter import *

##########################################################################
## modifed version of the Animation class that we used before           ##
## This file also contains utilities that are used throughout the game  ##
##########################################################################

class Animation(object):
    # Override these methods when creating your own animation
    def mousePressed(self, event): pass
    def keyPressed(self, event): pass
    def timerFired(self): pass
    def init(self): pass
    def redrawAll(self): pass
    
    def run(self, width=600, height=600):
        # create the root and the canvas
        self.root = Tk()
        self.width = width
        self.height = height
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        # set up events
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.redrawAll()
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()
        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()
        self.root.bind("<Button-1>", mousePressedWrapper)
        self.root.bind("<Key>", keyPressedWrapper)
        # set up timerFired events
        self.timerFiredDelay = 250 # milliseconds
        def timerFiredWrapper():
            self.timerFired()
            # redrawAllWrapper() removed because we want mutiple events to happen on the same screen
            # pause, then call timerFired again
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
        # init and get timerFired running
        self.init()
        redrawAllWrapper()
        timerFiredWrapper()
        # and launch the app
        self.root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

###############
## Utilities ##
###############

class PhysicalObject(object):
    def __init__(self, x, y, vx, vy, color, sideSize = 10):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.exists = True
        self.sideSize = sideSize

    def move(self):
        self.x += self.vx 
        self.y += self.vy

    def draw(self, canvas): # this should be overrided by each subclass of PhysicalObject 
                            # because not not all objects look the same
        canvas.create_rectangle(self.x - self.sideSize, self.y - self.sideSize, self.x + self.sideSize, self.y + self.sideSize, fill = self.color)

    def collides(self, other):
        x = self.sideSize + other.sideSize
        if(abs(self.x - other.x) <= x and abs(self.y - other.y) <= x):
            return True
        else:
            return False

def drawCountdownClock(canvas, x, y, size, maxTime, timeLeft):
    # print maxTime, timeLeft
    angle = timeLeft / maxTime * 360.0
    if(angle < 0): angle = 0
    color = "green" if angle > 90 else "red"\
    # print color
    canvas.create_arc(x - size, y - size, x + size, y + size, fill = color, extent = angle)
