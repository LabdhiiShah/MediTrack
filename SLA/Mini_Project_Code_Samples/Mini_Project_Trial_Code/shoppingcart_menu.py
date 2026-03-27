# importing only those functions 
# which are needed 
from tkinter import *
from tkinter.ttk import *
from time import strftime 

# creating tkinter window 
root = Tk() 
root.title('Menu Demonstration') 

# Creating Menubar 
menubar = Menu(root) 

# Adding File Menu and commands 
file = Menu(menubar, tearoff = 0) 
menubar.add_cascade(label ='File', menu = file) 
file.add_command(label ='New File', command = None) 
file.add_command(label ='Open...', command = None) 
file.add_command(label ='Save', command = None) 
file.add_separator() 
file.add_command(label ='Exit', command = root.destroy) 



# Adding shopping card menu button
scart = Menu(menubar, tearoff = 0) 
menubar.add_cascade(label ='CART', menu = scart) 



# display Menu 
root.config(menu = menubar) 
mainloop() 
