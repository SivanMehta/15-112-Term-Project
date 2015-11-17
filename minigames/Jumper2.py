###########################################################################################
## The player must maneuver around incoming enemies via jumping and moving right to left ##
###########################################################################################

from WarioAnimation import Animation, PhysicalObject
from Tkinter import *
import random, sys, time

class Jumper(PhysicalObject):
    def __init__(self, size):
        super(Jumper, self).__init__(300, 460, 0,0, "blue", size)

    def jump(self):
        self.vy -= 30

class Enemy(PhysicalObject):
    def __init__(self, size):
        direction = random.choice([1, -1])
        start = 10 if direction == 1 else 590
        super(Enemy, self).__init__(start, random.choice([490, 445]), 40 * direction, 0, "red", size)
        #the random part is the varying height (490 you must jump over and 445 you can either jump or stay pu)

    def move(self, width):
        super(Enemy, self).move()
        if(self.x > width or self.x < 0):
            self.exists = False

class JumperGame(Animation):
    def __init__(self, root, canvas, level = 1, height = 600, width = 600):
        self.root = root
        self.canvas = canvas
        self.level = level
        self.height = height
        self.floor = 480
        self.width = width
        self.initalTime = 7
        self.startTime = int(time.time()) % 10
        self.gravity = -10
        self.gameStatus = "playing"
        self.enemies = []
        self.enemyCount = 0
        self.jumper = Jumper(20) #change to continuously smaller

        self.root.bind("<Key>", self.keyPressed)

    def timerFired(self):
        #manage game conditions
        curTime = int(time.time()) % 10
        self.timeLeft =  (5 - (curTime - self.startTime)) % 10
        if(self.timeLeft > self.initalTime):
            self.timeLeft = 0

        if(self.enemyCount < self.level * 4):
             if random.uniform(0.0, 1.0) < .4 * (self.level / 10.0): #.1 is easy, .5 is hard
                 self.enemies.append(Enemy(10))
                 self.enemyCount += 1

        for enemy in self.enemies:
            if enemy.collides(self.jumper):
                self.gameStatus = "Lose"
        if(self.enemies == [] and self.enemyCount >= self.level * 4): #if all the enemies in the level have been jumped over
            self.gameStatus = "Win"

        # manage game elements
        # move all the enemies
        for enemy in self.enemies:
            enemy.move(self.width)
        # remove those who got past the end
        self.enemies = [e for e in self.enemies if e.exists]
        #move the jumper
        self.jumper.move()
        #check if on sides
        if(self.jumper.x >= 575):
            self.jumper.x = 575
            self.jumper.vx = 0
        if(self.jumper.x <= 25):
            self.jumper.x = 25
            self.jumper.vx = 0
        if(self.jumper.y >= self.floor): # if on floor
            self.jumper.y = self.floor
            self.jumper.vy = 0
        else: #gravity
            self.jumper.vy -= self.gravity
        self.jumper.vx /= 2.0 # pseudo not really but kinda sorta friction!
        if(abs(self.jumper.vx) < 0.1): #because having a speed of -4.76837158203e-06 is silly
            self.jumper.vx = 0

        self.redrawAll()

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.canvas.create_line(0,500,600,500)
        for enemy in self.enemies:
            enemy.draw(self.canvas)
        if(self.gameStatus == "playing"):
            self.canvas.create_text(300, 200, text = "Enemies Left: " + str(self.level * 4 - self.enemyCount))
        self.canvas.create_text(300, 100, text = "Avoid!", font = "Helvetica 75 bold")
        self.jumper.draw(self.canvas)

    def keyPressed(self,event):
        # print event.keysym
        if(self.jumper.y >= self.floor): #you can only jump when you're on the ground
            if(event.keysym == "Up"):
                self.jumper.jump()
                self.jumper.move()
        if(event.keysym == "Left"):
            self.jumper.vx -= 20
        if(event.keysym == "Right"):
            self.jumper.vx += 20

    def run(self):
        self.canvas.pack()