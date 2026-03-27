from tkinter import *
window = Tk()
frame1 = Frame(master=window, width=100, height=100, bg="red")
frame1.pack()
frame2 = Frame(master=window, width=50, height=50, bg="yellow")
frame2.pack()
frame3 = Frame(master=window, width=25, height=25, bg="blue")
frame3.pack()
window.mainloop()

