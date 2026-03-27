from tkinter import *
window = Tk()
window.title("Font Example")
window.geometry("300x200")

lbl1 = Label(window, text="Normal Font", font=("Arial", 12))
lbl1.pack()

lbl2 = Label(window, text="Bold Font", font=("Arial", 14, "bold"))
lbl2.pack()

lbl3 = Label(window, text="Italic Font", font=("Times New Roman", 16, "italic"))
lbl3.pack()

lbl4 = Label(window, text="Bold Italic Font", font=("Verdana", 18, "bold italic"))
lbl4.pack()

window.mainloop()