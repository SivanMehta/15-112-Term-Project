from WarioAnimation import Animation, PhysicalObject
from Tkinter import *
import random, sys, time

class Jumper(PhysicalObject):
    def __init__(self, size):
        super(Jumper, self).__init__(300, 460, 0,0, "blue", size)

    def jump(self):
        self.vy -= 25

class Enemy(PhysicalObject):
    def __init__(self, size):
        super(Enemy, self).__init__(10, 490, 25, 0, "red", size)

    def move(self, width):
        super(Enemy, self).move()
        if(self.x > width):
            self.exists = False

class JumperGame(Animation):
    def __init__(self, level = 1, height = 600, width = 600):
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
        # this allows the jumper size to get continually smaller, as the level increases, but with a minimum of 9)

    def timerFired(self):
        #manage game conditions
        curTime = int(time.time()) % 10
        self.timeLeft =  (5 - (curTime - self.startTime)) % 10
        if(self.timeLeft > self.initalTime):
            self.timeLeft = 0


        if(self.enemyCount < self.level):
             if random.uniform(0.0, 1.0) < .1 * (self.level / 10.0): #.1 is easy, .5 is hard
                 self.enemies.append(Enemy(10))
                 self.enemyCount += 1

        for enemy in self.enemies:
            if enemy.collides(self.jumper):
                self.gameStatus = "Lose"
        if(self.enemies == [] and self.enemyCount == self.level): #if all the enemies in the level have been jumped over
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
        else: #gravity!
            self.jumper.vy -= self.gravity
        self.jumper.vx /= 2.0 # pseudo not really but kinda sorta friction!
        if(abs(self.jumper.vx) < 0.1): #because having a speed of -4.76837158203e-06 is silly
            self.jumper.vx = 0

        self.redrawAll()
        if(self.gameStatus == "playing"):
            self.canvas.create_text(300, 200, text = "Enemies Left " + str(self.level - self.enemyCount))
            self.canvas.after(100, self.timerFired)
        else:
            self.canvas.create_text(300,300, text = "You " + self.gameStatus, fill = "red")

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.canvas.create_line(0,500,600,500)
        for enemy in self.enemies:
            enemy.draw(self.canvas)
        self.jumper.draw(self.canvas)

    def keyPressed(self,event):
        # print event.keysym
        if(self.jumper.y >= self.floor): #you can only jump when you're on the ground
            if(event.keysym == "Up"):
                self.jumper.jump()
                self.jumper.move()
        if(event.keysym == "Left"):
            self.jumper.vx -= 10
        if(event.keysym == "Right"):
            self.jumper.vx += 10

    def run(self, width = 600, height = 600):
        self.root = Tk()
        self.height = height
        self.width = width
        self.canvas = Canvas(self.root, width=self.width, height=height)
        self.canvas.pack()
        self.root.bind("<Key>", self.keyPressed)
        self.init()
        self.timerFired()
        self.root.mainloop()

JumperGame(10).run()