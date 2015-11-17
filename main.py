from Controller import Controller
from Tkinter import *

class game():
    def jail(self, event):
        pass

    def mousePressed(self, event):
        # print "here"
        if(125 <= event.x < 475 and 350 <= event.y <= 450): #if you clicked the button
            self.startGame()

    def startGame(self):
        # print "here"
        self.root.bind("<Button-1>", jail)
        Controller(self.root, self.canvas).run()

    def run(self):
        self.root = Tk()
        self.root.title("Sivan Mehta's Term Project")
        self.canvas = Canvas(self.root, width = 600, height = 600)
        self.canvas.pack()
        self.root.bind("<Button-1>", self.mousePressed)
        self.canvas.create_rectangle(0,0,600,600, fill = "blue") #background
        self.canvas.create_text(300, 100, text = "GAME SWITCHER", font = "Helvetica 25 bold", fill = 'white') #title
        self.canvas.create_rectangle(125, 350, 475, 450, fill = "red", activefill = "green") #button
        self.canvas.create_text(300, 400, text = "START", font = "Helvetica 75 bold")
        self.root.mainloop()

def jail(event):
    pass

if __name__ == "__main__":
    game().run()