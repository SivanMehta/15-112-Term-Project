from helpers.WarioAnimation import *
from Tkinter import *
import time, math, random
from helpers.Levels import *
from helpers.getDirection import getDirectionTowards

###############################################################
## Move the circle to the end of a given path towards a goal ##
###############################################################


class gravityGame(Animation):
    def __init__(self, root, canvas, level = 1, height = 600, width = 600):
        self.level = level % 7 # there are only 7 - 1 designed levels
        self.root = root
        self.height = height
        self.width = width
        self.canvas = canvas
        self.root.bind("<Key>", self.keyPressed)

        self.circleRadius = 10
        self.path = getPath(self.level)
        playersStart = getPlayerStart(self.level)
        goalStart = getGoalStart(self.level)
        self.blackHoles = getBlackHoles(self.level)
        self.promptLocation = getPromptLocation(self.level)
        self.player = PhysicalObject(playersStart[0],playersStart[1],0,0,"red")
        self.goal = PhysicalObject(goalStart[0],goalStart[1],0,0,"aquamarine", 20)

        self.startTime = time.time()
        self.initalTime = getLevelTime(self.level)
        self.timeLeft = self.initalTime
        
        self.gameStatus = "playing"
        self.forces = []


    def timerFired(self):
        self.canvas.delete(ALL)
        self.player.move()
        #apply friction
        self.player.vx *= .99
        self.player.vy *= .99
        if(self.player.vx <= .01): self.player.vx = 0
        if(self.player.vy <= .01): self.player.vy = 0

        curTime = time.time()
        self.timeLeft =  self.initalTime - (curTime - self.startTime)
        # if(self.timeLeft > self.initalTime):
        #     self.timeLeft = 0

        if(self.timeLeft < 0):
            self.gameStatus = "Lose"

        #apply black hole gravity
        for hole in self.blackHoles:
            #because the mass of the player is 1, and force = mass * acceleration, the acceleration = force (without units)
            force = hole.getForce(self.player)
            direction = getDirectionTowards(hole.x, hole.y, self.player.x, self.player.y)
            fx = force * direction[0]
            fy = force * direction[1]
            self.forces.append(force)
            # print fx, fy
            self.player.vx += fx
            self.player.vy += fy

        if(self.path.collides(self.player) == False):
            self.gameStatus = "Lose"

        if(self.goal.collides(self.player)):
            self.gameStatus = "Win"

        self.redrawAll()

    def redrawAll(self):
        self.path.draw(self.canvas)
        self.goal.draw(self.canvas)
        for hole in self.blackHoles:
            hole.draw(self.canvas)
        self.player.draw(self.canvas)
        # self.canvas.create_text(50,50, text = self.timeLeft)
        self.canvas.create_oval(524, 524, 576, 576, fill = "white", outline = "white")
        drawCountdownClock(self.canvas, 550, 550, 25, self.initalTime, self.timeLeft)
        self.canvas.create_text(self.promptLocation[0], self.promptLocation[1], text = "Move to Goal", font = "Helvetica 25 bold")

    def keyPressed(self, event):
        # print "click"
        if(event.keysym == "Up"):
            self.player.vy -= 10
        elif(event.keysym == "Down"):
            self.player.vy += 10
        elif(event.keysym == "Right"):
            self.player.vx += 10
        elif(event.keysym == "Left"):
            self.player.vx -= 10
        # elif(event.keysym == "f"):
        #     return self.forces
        #     sys.exit()

    def run(self):
        self.canvas.pack()