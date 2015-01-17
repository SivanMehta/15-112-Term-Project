from WarioAnimation import Animation
from Tkinter import *
import random, sys, time
from wordSearch import *

def printBoard(board):
    for row in board:
        for val in board:
            print val
        print 

################################
## Play a Game of Tic Tac Toe ##
################################

class ticTacToe(Animation):
    def __init__(self):
        self.board = [[None, None, None],
                      [None, None, None],
                      [None, None, None]]
        self.curPlayer = 'X' #the user is always Xs
        self.otherPlayer = 'O'
        self.gameStatus = "playing"
        self.startTime = int(time.time()) % 10
        self.initalTime = 10
        self.timeLeft = self.initalTime

    def timerFired(self):

        if(self.hasWon('XXX')):
            self.gameStatus = "Won"
        elif(self.hasWon('OOO') or self.timeLeft <= 0): # if someone has won
            self.gameStatus = "Lost"
        elif(self.isFull()): # if the board is full, it must be a tie
            self.gameStatus = "Lost"
        
        if(self.curPlayer == 'O' and self.gameStatus == "playing"): # if it is the computer's turn, make a random move
            moves = self.getMoves()
            if(len(moves) == 0):
                self.gameStatus = "Tied"
            else:
                selectedMove = moves[int(random.random() * len(moves))]
                row = selectedMove[0]
                col = selectedMove[1]
                self.board[row][col] = 'O'
            self.curPlayer,self.otherPlayer = self.otherPlayer, self.curPlayer

        curTime = int(time.time()) % 10
        self.timeLeft = self.timeLeft =  (5 - (curTime - self.startTime)) % 10
        if(self.timeLeft > self.initalTime):
            self.timeLeft = 0

        self.redrawAll()
        if(self.gameStatus == "playing"):
            self.canvas.after(10, self.timerFired)

    def getMoves(self):
        moves = []
        for row in xrange(3):
            for col in xrange(3):
                if(self.board[row][col] == None):
                    moves.append([row,col])
        return moves


    def isFull(self):
        for row in self.board:
            for val in row:
                if(val == None): return False
        return True

    def hasWon(self, player):
        # print "searching for: ", player
        return wordSearch(self.board, player)

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.drawBoard()
        self.drawLines()
        # print self.gameStatus
        if(self.gameStatus != "playing"):
            self.drawMessage()
        else:
            self.canvas.create_text(300, 350, text = "Time Left: " + str(self.timeLeft))
            

    def drawBoard(self):
        #given that the board is 600x600, draw a board
        for row in xrange(3):
            for col in xrange(3):
                if(self.board[row][col] != None):
                    self.canvas.create_text(100 + 200 * row,100 + 200 * col, text = self.board[row][col], font = "Helvetica 100 bold")

    def drawLines(self):
        self.canvas.create_line(200,0,200,600)
        self.canvas.create_line(400,0,400,600)
        self.canvas.create_line(0,200,600,200)
        self.canvas.create_line(0,400,600,400)

    def drawMessage(self):
        self.canvas.create_text(300,350, text = "You " + self.gameStatus)

    def mousePressed(self, event):
        # print event.y, event.x
        row = event.x / 200
        col = event.y / 200
        # print row, col

        # if the selected space is occupied, continue
        if(self.board[row][col] == None):
            self.board[row][col] = self.curPlayer
            self.curPlayer,self.otherPlayer = self.otherPlayer, self.curPlayer
        # printBoard(self.board)

    def run(self, level = 1, width = 600, height = 600):
        self.level = level
        self.root = Tk()
        self.height = height
        self.width = width
        self.canvas = Canvas(self.root, width=self.width, height=height)
        self.canvas.pack()
        self.root.bind("<Button-1>", self.mousePressed)
        self.init()
        self.timerFired()
        self.root.mainloop()

ticTacToe().run()