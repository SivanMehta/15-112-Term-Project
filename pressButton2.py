from WarioAnimation import *
from Tkinter import *
import random, sys, time

##########################################################################################################
## The user must click the button a given number of times, but if they press too many times, they loose ##
##########################################################################################################

class buttonPresser(Animation):
    def __init__(self, root, canvas, level = 1, width = 600, height = 600):
        self.level = level
        # print self.level
        self.height = height
        self.width = width
        self.root = root
        self.canvas = canvas
        self.radius = 75
        self.cx = 300
        self.cy = 300
        self.presses = 0
        self.goal = int(random.random() * 10 * self.level) + 10 # anything from 10 to 10 * level

        self.initalTime = int((self.level ** .15) + 5.0) # starts out at 5 and gradually gets larger
        self.timeLeft = self.initalTime
        self.gameStatus = "playing"
        self.startTime = time.time() # could start at any time

        self.root.bind("<Button-1>", self.mousePressed)

    def timerFired(self):
        curTime = time.time()
        self.timeLeft =  self.initalTime - (curTime - self.startTime)
        if(self.timeLeft > self.initalTime):
            self.timeLeft = 0

        if(self.goal == self.presses and self.timeLeft <= 0): # if you have not already lost
            self.gameStatus = "Win"
        elif(self.goal < self.presses):
            self.gameStatus = "Lose"
        elif(self.timeLeft <= 0):
            self.gameStatus = "Lose"

        self.redrawAll()

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.canvas.create_oval(self.cx - self.radius, self.cy - self.radius, self.cx + self.radius, self.cy + self.radius, fill = "red")
        self.canvas.create_text(300, 300, text = "CLICK ME", font = "Helvetica 25 bold")
        self.canvas.create_text(300, 475, text = "Score: " + str(self.presses), font = "Helvetica 25 bold")
        self.canvas.create_text(300, 100, text = "Goal: " + str(self.goal), font = "Helvetica 25 bold")
        # self.canvas.create_text(300, 550, text = "Time Left: " + str(self.timeLeft))
        drawCountdownClock(self.canvas, 300, 550, 25, self.initalTime * 1.0, self.timeLeft)
        # self.canvas.create_text(300, 50,  text = self.gameStatus)

    def mousePressed(self,event):
        if((self.cx - event.x) ** 2 + (self.cy - event.y) ** 2 <= self.radius ** 2):
            self.presses += 1

    def run(self):
        self.canvas.pack()
        self.init()