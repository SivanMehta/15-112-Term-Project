######################################################
## This was used to figure out how to import images ##
######################################################


from Tkinter import *


root = Tk()
canvas = Canvas(root, width = 600, height = 600)
canvas.pack()

heart = PhotoImage(file = "Heart.gif").subsample(2,2)
image = canvas.create_image(300, 300, image = heart)

root.mainloop()