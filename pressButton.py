from WarioAnimation import Animation
from Tkinter import *
import random, sys, time

##########################################################################################################
## The user must click the button a given number of times, but if they press too many times, they loose ##
##########################################################################################################

class buttonPresser(Animation):
    def init(self):
        self.radius = 75
        self.cx = 300
        self.cy = 300
        self.presses = 0
        self.goal = int(random.random() * 10 * self.level) + 1 # anything from 1 to 10 * level
        self.initalTime = 7
        self.timeLeft = self.initalTime
        self.gameStatus = "playing"
        self.startTime = int(time.time()) % 10 # could start at any time

    def timerFired(self):
        curTime = int(time.time()) % 10
        self.timeLeft =  (5 - (curTime - self.startTime)) % 10
        if(self.timeLeft > self.initalTime):
            self.timeLeft = 0

        if(self.goal == self.presses and self.gameStatus != "Lose"): # if you have not already lost
            self.gameStatus = "Win"
        elif(self.goal < self.presses):
            self.gameStatus = "Lose"
        elif(self.timeLeft <= 0):
            self.gameStatus = "Lose"

        self.redrawAll()
        if(self.gameStatus != "Lose"): # <-- because this game lasts until the end, not until you lose
            self.canvas.after(10, self.timerFired)

    def redrawAll(self):
        #draw button
        self.canvas.delete(ALL)
        self.canvas.create_oval(self.cx - self.radius, self.cy - self.radius, self.cx + self.radius, self.cy + self.radius, fill = "red")
        self.canvas.create_text(300, 300, text = "CLICK ME", font = "Helvetica 25 bold")
        self.canvas.create_text(300, 500, text = "Score: " + str(self.presses))
        self.canvas.create_text(300, 100, text = "Goal: " + str(self.goal))
        self.canvas.create_text(300, 550, text = "Time Left: " + str(self.timeLeft))
        self.canvas.create_text(300, 50,  text = self.gameStatus)

    def mousePressed(self,event):
        if((self.cx - event.x) ** 2 + (self.cy - event.y) ** 2 <= self.radius ** 2):
            self.presses += 1

    def run(self, level = 1, width = 600, height = 600):
        self.level = level
        self.root = Tk()
        self.height = height
        self.width = width
        self.canvas = Canvas(self.root, width=self.width, height=height)
        self.canvas.pack()
        self.root.bind("<Button-1>", self.mousePressed)
        self.init()
        self.timerFired()
        self.root.mainloop()

buttonPresser().run(4)