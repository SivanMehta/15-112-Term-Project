########################################################################################################
## This file is used exlusively by the gravity game to create and define the components of each level ##
########################################################################################################

from Tkinter import *

from helpers.WarioAnimation import PhysicalObject

class BlackHole(object):
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = self.radius = mass # for simplicity's sake, the mass = radius (ignoring units)

    def getForce(self, player):
        distance = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** .5 #distance formula
        # to make things easy, we will simplfy the Universal law of Gravitation by making the mass of the player = 1 and G = 500
        force = 500 * self.mass / (distance ** 2)
        return force

    def draw(self, canvas):
        # canvas.create_oval(self.x - self.mass, self.y - self.mass, self.x + self.mass, self.y + self.mass, fill = "black")
        self.hole = PhotoImage(file = "Hole.gif")#.zoom(8,8).subsample(1024/self.mass, 1024/self.mass)
        image = canvas.create_image(self.x, self.y, image = self.hole)

class Path(object):
    def __init__(self, *pieces):
        self.pieces = pieces

    def draw(self, canvas):
        for piece in self.pieces:
            piece.draw(canvas)

    def collides(self, player):
        for piece in self.pieces:
            if(piece.collides(player)):
                return True
        return False

class RectPiece(object):
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = "black"

    def collides(self, player): #player is a PhysicalObject
        if( (self.x0 < player.x < self.x1) and # if outside the sides
            (self.y0 < player.y < self.y1) ): # if outside the insides
            return True
        return False

    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill = self.color)

# level definitions

paths = []
blackHoles = []
prompts = []

piece1_1 = RectPiece(250,0,350,600)
hole1_1 = BlackHole(100,200, 20)
hole1_2 = BlackHole(500,400, 20)
prompt1 = [100, 550]
paths.append(Path(piece1_1))
blackHoles.append([hole1_1, hole1_2])
prompts.append(prompt1)

piece2_1 = RectPiece(100,200,200,600)
piece2_2 = RectPiece(100,200,500,300)
piece2_3 = RectPiece(400,0,500,300)
hole2_1 = BlackHole(450, 500, 20)
hole2_2 = BlackHole(150, 100, 30)
prompt2 = [300, 550]
paths.append(Path(piece2_1, piece2_2, piece2_3))
blackHoles.append([hole2_1, hole2_2])
prompts.append(prompt2)

piece3_1 = RectPiece(100,200,200,600)
piece3_2 = RectPiece(200,200,500,300)
piece3_3 = RectPiece(400,300,500,600)
hole3_1 = BlackHole(300,550, 10)
prompt3 = [300, 50]
paths.append(Path(piece3_1, piece3_2, piece3_3))
blackHoles.append([hole3_1])
prompts.append(prompt3)

piece4_1 = RectPiece(0, 475, 525, 550)
piece4_2 = RectPiece(450,50, 525, 475)
piece4_3 = RectPiece(50, 50, 450, 125)
piece4_4 = RectPiece(50,125, 125, 425)
piece4_5 = RectPiece(125,350,350, 425)
piece4_6 = RectPiece(250,250,350,350)
hole4_1 = BlackHole(200,200, 10)
hole4_2 = BlackHole(400,200, 10)
hole4_3 = BlackHole(400, 400, 10)
prompt4 = [300, 25]
paths.append(Path(piece4_1, piece4_2, piece4_3, piece4_4, piece4_5, piece4_6))
blackHoles.append([hole4_1, hole4_2, hole4_3])
prompts.append(prompt4)

piece5_1 = RectPiece(250, 50, 350, 400)
hole5_1 = BlackHole(300, 1300, 800)
prompt5 = [100, 50]
paths.append(Path(piece5_1))
blackHoles.append([hole5_1])
prompts.append(prompt5)

piece6_1 = RectPiece(0, 500, 200, 600)
piece6_2 = RectPiece(100, 300, 200, 500)
piece6_3 = RectPiece(200, 300, 400, 400)
piece6_4 = RectPiece(300, 100, 400, 300)
piece6_5 = RectPiece(400, 100, 600, 200)
piece6_6 = RectPiece(500, 0, 600, 100)
hole6_1 = BlackHole(50,50,50)
hole6_2 = BlackHole(550, 500, 50)
prompt6 = [300, 550]
paths.append(Path(piece6_1, piece6_2, piece6_3, piece6_4, piece6_5, piece6_6))
blackHoles.append([hole6_1, hole6_2])
prompts.append(prompt6)

def getPath(level):
    return paths[level - 1]

def getPlayerStart(level):
    if(level == 1):
        return [300, 100]
    if(level == 2):
        return [150, 500]
    if(level == 3):
        return [450,500]
    if(level == 4):
        return [300, 300]
    if(level == 5):
        return [300, 300]
    if(level == 6):
        return [50, 550]

def getGoalStart(level):
    if(level == 1):
        return [300, 500]
    if(level == 2):
        return [450, 100]
    if(level == 3):
        return [150, 550]
    if(level == 4):
        return [100, 515]
    if(level == 5):
        return [300, 75]
    if(level == 6):
        return [550, 50]

def getLevelTime(level):
    if(level == 1):
        return 4
    if(level == 2):
        return 8
    if(level == 3):
        return 10
    if(level == 4):
        return 15
    if(level == 5):
        return 4
    if(level == 6):
        return 10

def getBlackHoles(level):
    return blackHoles[level - 1]

def getPromptLocation(level):
    return prompts[level - 1]