from tkinter import * 
from tkinter.ttk import *
window = Tk()
window.geometry("400x300")
window.title("Label Demo")
label = Label(window, text ="LABEL1")
bttn1 = Button(window, text = "BUTTON1")
bttn1.pack()
"""

text = StringVar()
text.set("This is the default text")
text="Hi"
textBox = Entry(window,textvariable = text)
textBox.pack()
"""
txt1 = Entry(window)
#txt1.config(state=DISABLED)
txt1.pack()
#Setting Default Text of Entry Widget
#txt1.insert(0, "This is the default text")
window.mainloop()