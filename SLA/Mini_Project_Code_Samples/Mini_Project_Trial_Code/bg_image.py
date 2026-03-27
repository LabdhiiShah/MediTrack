import tkinter
from tkinter import *
from PIL import Image, ImageTk
root = Tk()
frame=Frame(root)
frame.pack(fill=BOTH,expand=True)
#root.geometry("300x300")
# Create a photoimage object of the image in the path
image1 = Image.open("bird.png")
test = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(frame,image=test)
#label1.image = test
# Position image
#label1.place(x=0, y=0)
label1.pack(side=LEFT,fill=BOTH,expand=True)
#root.resizable(False, False)# resize x and y direction
root.mainloop()