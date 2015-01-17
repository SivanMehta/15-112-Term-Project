###############################################################
## This is the file that represented the intermediary screen ##
## and also generally controls the flow of the game          ##
###############################################################


from Tkinter import *
import time, random, copy

from WarioAnimation import *
from circleChaser2 import circleChaser
from pressButton2 import buttonPresser
from TicTacToe2 import ticTacToe
from Jumper2 import *
from placeCircle2 import circleGame
from gravityGame2 import gravityGame
# import main

class Controller(Animation):
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.level = 1
        self.width = 600
        self.height = 600
        # self.root = Tk()
        # self.canvas = Canvas(self.root, width = self.width , height = self.width)
        self.startTime = int(time.time())
        self.isGameOver = False
        self.root.bind("<Key>", self.keyPressed)

        self.score = 0
        self.lives = 3
        self.hearts = []
        self.currentGame = None
        self.currentGameStatus = None

        self.initalTime = 4
        self.timeLeft = self.initalTime
        self.startTime = time.time()
        self.timeLeft = self.initalTime - (time.time() - self.startTime) #same as elapsed since start

        self.games = [circleChaser, buttonPresser, ticTacToe, JumperGame, circleGame, gravityGame]
        self.gamesLeft = copy.copy(self.games)

    def timerFired(self):
        # print self.currentGame == None
        # print self.gamesLeft
        # print self.timeLeft
        if(int(self.timeLeft) == 0 and self.timeLeft < 0): #if the timer is out
            if(self.currentGame == None): # if there is no current game
                if(len(self.gamesLeft) == 0):
                    self.level += 1
                    self.gamesLeft = copy.copy(self.games)

                # for debugging:
                # self.currentGame = circleChaser(self.root, self.canvas, self.level, self.width, self.height)
                # self.currentGame = buttonPresser(self.root, self.canvas, self.level, self.width, self.height)
                # self.currentGame = ticTacToe(self.root, self.canvas, self.level, self.width, self.height)
                # self.currentGame = JumperGame(self.root, self.canvas, self.level, self.width, self.height)
                # self.currentGame = circleGame(self.root, self.canvas, self.level, self.width, self.height)
                # self.currentGame = gravityGame(self.root, self.canvas, self.level, self.width, self.height)

                gameChoice = random.choice(self.gamesLeft)
                self.currentGame = gameChoice(self.root, self.canvas, self.level, self.width, self.height)
                self.gamesLeft.remove(gameChoice)

                self.currentGame.run()
                self.currentGameStatus = self.currentGame.gameStatus
            else: #if a game must running
                self.currentGameStatus = self.currentGame.gameStatus
                # print self.currentGameStatus
                if(self.currentGameStatus != "playing"): # if the game is over
                    # print "finished game"
                    # print "here"
                    self.score += 1 * (self.currentGameStatus == "Win") # if you won the game, add to the score
                    self.lives -= 1 * (self.currentGameStatus == "Lose") # if you lost the game, subtract a life
                    
                    #reset the controller
                    self.currentGame = None
                    self.currentGameStatus = None
                    self.startTime = time.time()
                    self.timeLeft = self.initalTime - (time.time() - self.startTime)
                    self.hearts = []

                    #remove and reset the controls
                    self.canvas.bind("<Button-1>", self.jail)
                    self.canvas.bind("<B1-Motion>", self.jail)
                    self.root.bind("<B1-ButtonRelease>", self.jail)
                    self.root.bind("<Key>", self.keyPressed)
                    if(self.score % len(self.games) == 0 and self.score != 0): # if you have played through all the games
                        self.level += 1
                        self.initalTime = 2 / (self.level) + 2
                else:
                    self.currentGame.timerFired()
        else: #if there is still time left between games, decrement timer
            curTime = time.time()
            self.timeLeft =  self.initalTime - (curTime - self.startTime)
            if(self.timeLeft > self.initalTime):
                self.timeLeft = 0
            self.redrawAll()
            # self.initalTime = int((10.0 / self.level) + 3)

        if(self.lives > 0):
            self.canvas.after(100, self.timerFired)
        else:
            self.redrawAll()
            self.drawGameOver()
            # self.saveHighScore()
            self.isGameOver = True

    def saveHighScore(self):
        print "saving high score ..."
        if(self.score > self.highScore):
            f = open('highscore.txt', 'w')
            f.write(str(self.highScore))
            # f.close()

    def keyPressed(self, event):
        if(event.keysym == "q"):
            self.lives == 0
        if(event.keysym == 'r' and self.isGameOver):
            self.__init__(self.root, self.canvas)
            self.timerFired()

    def jail(self, event): # placeholder for controls between gamess
        pass

    def drawGameOver(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0,0,600,600, fill = "#00FFFE")
        self.canvas.create_rectangle(100,100,500,500, fill = "red")
        self.canvas.create_text(300, 200, text = "GAME", font = "Helvetica 75 bold")
        self.canvas.create_text(300, 300, text = "OVER", font = "Helvetica 75 bold")
        self.canvas.create_text(300, 400, text = "Score: " + str(self.score), font = "Helvetica 75 bold")
        self.canvas.create_text(300, 550, text = "Press 'r' to restart")

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0, 0, 600, 600, fill = "white")
        self.canvas.create_text(300, 100, text = "Level: " + str(self.level), font = "Helvetica 75 bold")
        self.canvas.create_text(300, 200, text = "Score: " + str(self.score), font = "Helvetica 75 bold")
        # self.canvas.create_text(300, 275, text = "Lives: ")
        for life in xrange(self.lives):
            self.drawHeart(225 + 75 * life, 325)
        drawCountdownClock(self.canvas, 300, 450, 50, self.initalTime * 1.0, self.timeLeft)

    def drawHeart(self, x, y):
        # print "here"
        heart = PhotoImage(file = "Heart.gif").subsample(3,3) # to make the image 50 x 50
        self.hearts.append(heart) #because we need to save each heart for it to show itself
        image = self.canvas.create_image(x, y, image = heart)

    def run(self):
        self.timerFired()
        self.canvas.pack()
        

