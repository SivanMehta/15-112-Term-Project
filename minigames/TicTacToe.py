from helpers.WarioAnimation import *
from Tkinter import *
import random, sys, time
from helpers.wordSearch import *

def printBoard(board):
    for row in board:
        for val in board:
            print val
        print 

#################################
## Plays a Game of Tic Tac Toe ##
#################################

class ticTacToe(Animation):
    def __init__(self, root, canvas, level = 1, width = 600, height = 600):
        self.canvas = canvas
        self.root = root
        self.board = [[None, None, None],
                      [None, None, None],
                      [None, None, None]]
        self.curPlayer = 'X' #the user is always Xs
        self.otherPlayer = 'O'
        self.gameStatus = "playing"

        self.startTime = time.time()
        self.initalTime = 5.0 / level + 3
        self.timeLeft = self.initalTime

        self.level = level
        # self.root = Tk()
        self.height = height
        self.width = width
        self.level = level
        self.root.bind("<Button-1>", self.mousePressed)

    def run(self):
        # self.level = level
        # self.root = Tk()
        # self.height = height
        # self.width = width
        # self.canvas = Canvas(self.root, width=self.width, height=height)
        self.canvas.pack()
        # self.root.bind("<Button-1>", self.mousePressed)
        # self.init()
        # self.timerFired()
        # self.root.mainloop()

    def timerFired(self):

        if(self.hasWon('XXX')):
            self.gameStatus = "Win"
        elif(self.hasWon('OOO') or self.timeLeft <= 0): # if someone has won
            self.gameStatus = "Lose"
        elif(self.isFull()): # if the board is full, it must be a tie
            self.gameStatus = "Lose"
        
        if(self.curPlayer == 'O' and self.gameStatus == "playing"): # if it is the computer's turn, make a random move
            moves = self.getMoves()
            if(len(moves) == 0):
                self.gameStatus = "Lose"
            else:
                selectedMove = moves[int(random.random() * len(moves))]
                row = selectedMove[0]
                col = selectedMove[1]
                self.board[row][col] = 'O'
            self.curPlayer, self.otherPlayer = self.otherPlayer, self.curPlayer

        curTime = time.time()
        self.timeLeft =  self.initalTime - (curTime - self.startTime)
        if(self.timeLeft > self.initalTime):
            self.timeLeft = 0

        self.redrawAll()

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
        # self.canvas.create_text(300, 350, text = "Time Left: " + str(self.timeLeft))
        self.canvas.create_text(300, 25, text = "TIC TAC TOE!", font = "Helvetica 25 bold")
        drawCountdownClock(self.canvas, 300, 550, 25, self.initalTime, self.timeLeft)


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