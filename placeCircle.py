from WarioAnimation import Animation
from Tkinter import *
import random
import time

#####################################################################
## The player must place a circle inside of randomly placed square ##
######################################################################

class circleGame(Animation):
    def init(self):
        self.squareSideSize = (10/self.level + 3) * 3 # this allows the square size to get continually smaller, as the level increases, but with a minimum of 9
        self.squareNW = [int(random.random() * (self.width - self.squareSideSize)), int(random.random() * (self.height - self.squareSideSize))]
        self.circleRadius = (10/self.level + 2) # same methodology as above, but with a minimum of 4
        self.circleCenter = [int(random.random() * (self.width - self.circleRadius)), int(random.random() * (self.height - self.circleRadius))]

        #if we placed the circle in the square, randomly place it somewhere else
        if((self.circleCenter[0] - self.squareNW[0]) < (self.squareSideSize - self.circleRadius) and
            (self.circleCenter[1] - self.squareNW[1]) < (self.squareSideSize - self.circleRadius)):
            self.circleCenter = [int(random.random() * (self.width - self.circleRadius)), int(random.random() * (self.height - self.circleRadius))]

        # print self.circleCenter
        self.startTime = time.time()
        self.timeLeft = 8
        self.gameStatus = "playing"

    def redrawAll(self):
        self.canvas.create_rectangle(self.squareNW[0], self.squareNW[1], self.squareNW[0] + self.squareSideSize, self.squareNW[1] + self.squareSideSize, fill = "red")
        self.canvas.create_oval(self.circleCenter[0] - self.circleRadius, self.circleCenter[1] - self.circleRadius, self.circleCenter[0] + self.circleRadius, self.circleCenter[1] + self.circleRadius, fill= "white")
        self.canvas.create_text(300, 550, text = self.timeLeft)

    def timerFired(self):
        self.canvas.delete(ALL)

        if(abs(self.circleCenter[0] - self.squareNW[0]) < (self.squareSideSize - self.circleRadius) and
            abs(self.circleCenter[1] - self.squareNW[1]) < (self.squareSideSize - self.circleRadius)): # same condition as before
                self.gameStatus = "Won"

        if(self.timeLeft != 0):
            curTime = int(time.time()) % 10
            self.timeLeft =  int(8 - (curTime - self.startTime)) % 10
        else:
            self.gameStatus = "Lose"

        self.redrawAll()
        if(self.gameStatus == "playing"): #if the game is not over, keep looping
            self.canvas.after(1, self.timerFired)
        else:
            self.canvas.create_text(300,300, text = "You " + self.gameStatus)

    def keyPressed(self, event):
        # print "here"
        if(event.keysym == "Up"):
            self.circleCenter[1] -= 10
        elif(event.keysym == "Down"):
            self.circleCenter[1] += 10
        elif(event.keysym == "Right"):
            self.circleCenter[0] += 10
        elif(event.keysym == "Left"):
            self.circleCenter[0] -= 10

        if(self.circleCenter[0] < 0):
            self.circleCenter[0] = 0
        elif(self.circleCenter[0] > self.width - self.circleRadius):
            self.circleCenter[0] = self.width - self.circleRadius
        if(self.circleCenter[1] < 0):
            self.circleCenter[1] = 0
        elif(self.circleCenter[1] > self.height - self.circleRadius):
            self.circleCenter[1] = self.height - self.circleRadius

    def run(self, level = 1, width = 600, height = 600):
        self.level = level
        self.root = Tk()
        self.height = height
        self.width = width
        self.canvas = Canvas(self.root, width=self.width, height=height)
        self.canvas.pack()
        self.root.bind("<Key>", self.keyPressed)
        self.init()
        self.timerFired()
        self.root.mainloop()

circleGame().run(1)