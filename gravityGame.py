from WarioAnimation import Animation, PhysicalObject
from Tkinter import *
import time, math, random
from Levels import getPath, getPlayerStart, getGoalStart, getBlackHoles
from getDirection import getDirectionTowards

################################################
## Move the circle to the end of a given path ##
################################################

class gravityGame(Animation):
    def init(self, level):
        self.circleRadius = 10
        self.path = getPath(level)
        playersStart = getPlayerStart(level)
        goalStart = getGoalStart(level)
        self.blackHoles = getBlackHoles(level)
        self.player = PhysicalObject(playersStart[0],playersStart[1],0,0,"red")
        self.goal = PhysicalObject(goalStart[0],goalStart[1],0,0,"aquamarine", 20)
        
        self.gameStatus = "playing"
        self.forces = []


    def timerFired(self):
        self.canvas.delete(ALL)
        self.player.move()
        #apply friction
        self.player.vx /= 2
        self.player.vy /= 2
        if(self.player.vx <= .01): self.player.vx = 0
        if(self.player.vy <= .01): self.player.vy = 0
        # if(0 < self.player.x < 600 == False): self.player.vx = 0
        # if(0 < self.player.y < 600 == False): self.player.vy = 0

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

        # if(self.timeLeft != 0):
        #     curTime = int(time.time()) % 10
        #     self.timeLeft =  int(self.initalTime - (curTime - self.startTime)) % 10
        # else:
            # self.gameStatus = "Lose"

        if(self.path.collides(self.player) == False):
            self.gameStatus = "Lose"

        if(self.goal.collides(self.player)):
            self.gameStatus = "Win"

        self.redrawAll()
        # print self.gameStatus
        if(self.gameStatus == "playing"):
            self.canvas.after(10, self.timerFired)

    def redrawAll(self):
        self.path.draw(self.canvas)
        self.goal.draw(self.canvas)
        for hole in self.blackHoles:
            hole.draw(self.canvas)
        self.player.draw(self.canvas)
        # self.canvas.create_text(50,50, text =  self.timeLeft)

    def keyPressed(self, event):
        # print "click"
        if(event.keysym == "Up"):
            self.player.vy -= 20
        elif(event.keysym == "Down"):
            self.player.vy += 20
        elif(event.keysym == "Right"):
            self.player.vx += 20
        elif(event.keysym == "Left"):
            self.player.vx -= 20
        elif(event.keysym == "f"):
            return self.forces
            sys.exit()

    def run(self, level = 1, width = 600, height = 600):
        self.level = level
        self.root = Tk()
        self.height = height
        self.width = width
        self.canvas = Canvas(self.root, width=self.width, height=height)
        self.canvas.pack()
        self.root.bind("<Key>", self.keyPressed)
        self.init(level)
        self.timerFired()
        self.root.mainloop()


gravityGame().run(6)#int(random.random() * 4))