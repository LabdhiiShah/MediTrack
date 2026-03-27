from tkinter import * 
from tkinter.ttk import *
  
# creating tkinter window 
root = Tk() 
  
# Adding widgets to the root window 
Label(root, text = 'Image Demo', font =( 
  'Verdana', 15)).pack(side = TOP, pady = 10) 
  
# Creating a photoimage object to use image 
photo = PhotoImage(file = r"bird.png")
#C:\\Users\\manis\\OneDrive\\Desktop\\python2024\\tkinter\\bird.png 
  
# here, image option is used to 
# set image on button 
Button(root, text = 'Click Me !',compound = LEFT, image = photo,).pack(side = TOP) 
#compund=LEFT will put image at left and text at right side  
mainloop() 