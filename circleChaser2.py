################################################################################################
## The user click onto a circle. after clicking it, the circle begins to move and if you move ##
## off of it before the timer is over, you lose                                               ##
################################################################################################

from WarioAnimation import *
from Tkinter import *
import random, time, math

class circleChaser(Animation):
    def __init__(self, root, canvas, level = 1, width = 600, height = 600):
        #set the initial values
        self.level = level
        self.height = height
        self.width = width
        self.root = root
        self.canvas = canvas

        # key bindings
        self.root.bind("<Button-1>", self.mousePressed)
        self.canvas.bind("<B1-Motion>", self.rightMouseMoved)
        self.root.bind("<B1-ButtonRelease>", self.rightMouseReleased)
        self.root.bind("<Key>", self.keyPressed)
        
        self.circleRadius = (10.0/self.level + 3) * 6
        self.circleCenter = [int(random.random() * (self.width - 200) + 200), int(random.random() * (self.height - 200) + 200)]
        
        randomDirection = int(random.random() * 10) #random number from [-2pi to 2pi]
        self.direction = [int(math.cos(randomDirection) * 10) * self.level, int(math.sin(randomDirection) * 10) * self.level]
        
        self.gameStarted = False
        self.initalTime = int((self.level ** .5) * 5.0)
        self.timeLeft = int(self.initalTime)
        
        self.gameStatus = "playing"
        self.mouse = [0, 0]

    def moveCircle(self):
        self.circleCenter[0] += self.direction[0]
        self.circleCenter[1] += self.direction[1]

    def mousePressed(self, event):
        # print "mousePressed"
        if((self.circleCenter[0] - event.x) ** 2 + (self.circleCenter[1] - event.y) ** 2 <= self.circleRadius ** 2
            and self.gameStarted == False): # if you pressed inside the circle while the game has not started
            self.gameStarted = True
            self.mouse = [event.x, event.y]
            self.startTime = int(time.time())

    def rightMouseMoved(self, event):
        # print "hello!"
        self.mouse = [event.x, event.y]

    def rightMouseReleased(self, event):
        if (self.gameStarted): #and self.gameStatus != "Win"): #if you let go after the game has started
            self.gameStatus = "Lose"

    def timerFired(self):
        # print self.direction
        if(self.gameStarted):
            if(self.timeLeft > 0):
                # curTime = int(time.time()) % 10
                # self.timeLeft =  (self.initalTime - (curTime - self.startTime)) % 10
                # if(self.timeLeft > self.initalTime):
                #     self.timeLeft = 0

                curTime = time.time()
                self.timeLeft =  self.initalTime - (curTime - self.startTime)
                if(self.timeLeft > self.initalTime):
                    self.timeLeft = 0

        #move and bounce the circle
        if(self.gameStarted):
            self.moveCircle()
        if(self.circleCenter[0] < self.circleRadius or self.circleCenter[0] > self.width - self.circleRadius):
            self.direction[0] *= -1
        if(self.circleCenter[1] < self.circleRadius or self.circleCenter[1] > self.height - self.circleRadius):
            self.direction[1] *= -1

        if(self.gameStarted == True and ((self.circleCenter[0] - self.mouse[0]) ** 2 + (self.circleCenter[1] - self.mouse[1]) ** 2 > self.circleRadius ** 2)): # if at any point after the game has started you move outside, you lose
            self.gameStatus = "Lose"

        if(self.timeLeft <= 0 and self.gameStatus != "Lose"):
            self.gameStatus = "Win"
            # self.gameStarted = False

        # if(self.gameStatus != "playing"):
        #     print "you " + self.gameStatus

        self.redrawAll()
        #if(self.gameStatus == "playing"): #if the game is not over, keep looping
         #   self.canvas.after(50, self.timerFired)

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.canvas.create_oval(self.circleCenter[0] - self.circleRadius,
                                self.circleCenter[1] - self.circleRadius,
                                self.circleCenter[0] + self.circleRadius, 
                                self.circleCenter[1] + self.circleRadius, 
                                fill= "green")
        # self.canvas.create_text(100, 100, text = self.timeLeft)
        drawCountdownClock(self.canvas, 300, 550, 25, self.initalTime * 1.0, self.timeLeft)
        if(self.gameStarted == False):
            self.canvas.create_text(300, 300, text = "Click and \n don't let go!", font = "Helvetica 25 bold")

    # def keyPressed(self, event):
    #     # print "here"
    #     self.timerFired()

    def run(self):
        self.canvas.pack()