from helpers.WarioAnimation import *
from Tkinter import *
import random
import time

#####################################################################
## The player must place a circle inside of randomly placed square ##
######################################################################

class circleGame(Animation):
    def __init__(self, root, canvas, level = 1, height = 600, width = 600):
        self.level = level
        self.root = root
        self.height = height
        self.width = width
        self.canvas = canvas
        self.root.bind("<Key>", self.keyPressed)

        self.vx = 0
        self.vy = 0

        self.squareSideSize = (10/self.level + 3) * 3 # this allows the square size to get continually smaller, as the level increases, but with a minimum of 9
        self.squareNW = [int(random.random() * (self.width - self.squareSideSize)), int(random.random() * (self.height - self.squareSideSize + 50))] # the + 50 is because we don't want to overlap the directions with the destination
        self.circleRadius = (10/self.level + 2) # same methodology as above, but with a minimum of 4
        self.circleCenter = [int(random.random() * (self.width - self.circleRadius)), int(random.random() * (self.height - self.circleRadius))]

        #if we placed the circle in the square, randomly place it somewhere else
        if((self.circleCenter[0] - self.squareNW[0]) < (self.squareSideSize - self.circleRadius) and
            (self.circleCenter[1] - self.squareNW[1]) < (self.squareSideSize - self.circleRadius)):
            self.circleCenter = [int(random.random() * (self.width - self.circleRadius)), int(random.random() * (self.height - self.circleRadius))]

        # print self.circleCenter
        self.startTime = time.time()
        self.initialTime = 5.0 / self.level + 4
        self.timeLeft = self.initialTime
        self.gameStatus = "playing"

    def redrawAll(self):
        self.canvas.create_rectangle(self.squareNW[0], self.squareNW[1], self.squareNW[0] + self.squareSideSize, self.squareNW[1] + self.squareSideSize, fill = "red")
        self.canvas.create_oval(self.circleCenter[0] - self.circleRadius, self.circleCenter[1] - self.circleRadius, self.circleCenter[0] + self.circleRadius, self.circleCenter[1] + self.circleRadius, fill= "white")
        self.canvas.create_text(300, 50, text = "Place circle in square", font = "Helvetica 25 bold")
        drawCountdownClock(self.canvas, 300, 550, 25, self.initialTime, self.timeLeft)

    def timerFired(self):
        self.canvas.delete(ALL)

        self.move()
        self.vx /= 2.0
        self.vy /= 2.0 # a silly version of friction
        if(abs(self.vx) < 0.1): #because having a speed of -4.76837158203e-06 is silly
            self.vx = 0
        if(abs(self.vy) < 0.1):
            self.vy = 0

        if(abs(self.circleCenter[0] - self.squareNW[0]) < (self.squareSideSize - self.circleRadius) and
            abs(self.circleCenter[1] - self.squareNW[1]) < (self.squareSideSize - self.circleRadius)): # if the circle is inside the square
                self.gameStatus = "Win"

        if(self.timeLeft > 0):
            curTime = time.time()
            self.timeLeft =  self.initialTime - (curTime - self.startTime)
            if(self.timeLeft > self.initialTime):
                self.timeLeft = 0
        else:
            self.gameStatus = "Lose"

        self.redrawAll()

    def move(self):
        self.circleCenter[0] += self.vx
        self.circleCenter[1] += self.vy

    def keyPressed(self, event):
        # print "here"
        if(event.keysym == "Up"):
            self.vy -= 10
        elif(event.keysym == "Down"):
            self.vy += 10
        elif(event.keysym == "Right"):
            self.vx += 10
        elif(event.keysym == "Left"):
            self.vx -= 10

        if(self.circleCenter[0] < 0):
            self.circleCenter[0] = 0
        elif(self.circleCenter[0] > self.width - self.circleRadius):
            self.circleCenter[0] = self.width - self.circleRadius
        if(self.circleCenter[1] < 0):
            self.circleCenter[1] = 0
        elif(self.circleCenter[1] > self.height - self.circleRadius):
            self.circleCenter[1] = self.height - self.circleRadius

    def run(self):
        self.canvas.pack()
        # self.init()