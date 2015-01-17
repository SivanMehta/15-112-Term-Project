################################################################################################
## This is a modified version of the one created in class, I used it to learn how develop the ##
## proper interaction between the Controller and a game                                       ##
################################################################################################

from Tkinter import *
import random, sys
from WarioAnimation import PhysicalObject

class Invader(PhysicalObject):
    def __init__(self, level):
        super(Invader, self).__init__(0,0, level * 5, 0, "red")

    def move(self, width):
        super(Invader, self).move()
        if(self.x > width or self.x < 0):
            self.vx = -self.vx
            self.y += 20

class Ship(PhysicalObject):
    def __init__(self, width, height):
        super(Ship, self).__init__(width / 2, height, 0, 0, "green")

    def move(self, width):
        if(self.x < 0):
            self.x = 10
            self.vx = 0
        if(self. x > width):
            self.x = width - 10
            self.vx = 0
        else:
            self.x += self.vx

class Bullet(PhysicalObject):
    def __init__(self, x, y):
        super(Bullet, self).__init__(x, y, 0, -20, "green")

    def move(self):
        super(Bullet, self).move()
        if(self.y < 0):
            self.exists = False

class ShooterGame(object):
    def __init__(self, width = 600, height = 600, level = 1):
        self.width = width
        self.height = height
        self.ship = Ship(self.width, self.height)
        self.enemies = []
        self.bullets = []
        self.isGameOver = False
        self.enemyCount = 0
        self.level = level
        self.gameStatus = "playing"

    def timerFired(self):
        # print "game timer"
        # move everything
        self.ship.move(self.width)
        for bullet in self.bullets:
            bullet.move()
        for enemy in self.enemies:
            enemy.move(self.width)

        if(self.enemyCount < self.level):
            if random.uniform(0.0, 1.0) < 0.2:
                self.enemies.append(Invader(self.level))
                self.enemyCount += 1
        elif(self.enemyCount == self.level):
            if(self.enemies == []): # if you have killed all the enemies
                self.isGameOver = True
                self.gameStatus = "Win"

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.collides(enemy):
                    bullet.exists = False
                    enemy.exists = False

        for enemy in self.enemies:
            if enemy.collides(self.ship):
                self.isGameOver = True
                self.gameStatus = "Lose"

        #only save the bullets that exist

        self.bullets = [b for b in self.bullets if b.exists]
        self.enemies = [e for e in self.enemies if e.exists]

        if(self.isGameOver):
            # self.canvas.create_text(self.width / 2, self.height / 2, text= "Game Over")
            if(self.gameStatus != "playing"):
                self.message = "You Win"
            else: 
                self.message = "You Lose"
            # self.root.destroy()
            return

        # print "drawing game"
        self.redrawAll()
        if(self.gameStatus == "playing"):
            self.canvas.after(100, self.timerFired)
        # this was removed because the continuous firing should only take place in the controller


    def keyPressed(self, event):
        # print "pressed key"
        if event.keysym == "Left":
            self.ship.x -= 8
        elif event.keysym == "Right":
            self.ship.x += 8
        elif event.keysym == "space":
            self.bullets.append(Bullet(self.ship.x, self.ship.y))
    
    def redrawAll(self):
        self.canvas.delete(ALL)
        self.ship.draw(self.canvas)
        for bullet in self.bullets:
            bullet.draw(self.canvas)
        for enemy in self.enemies:
            enemy.draw(self.canvas)
        if(self.isGameOver):
            self.canvas.create_text(300, 300, text = self.message)

    def run(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.root.bind("<Key>", self.keyPressed)
        # print "bound keys"
        result = self.timerFired()
        self.root.mainloop()
        return result

ShooterGame().run()