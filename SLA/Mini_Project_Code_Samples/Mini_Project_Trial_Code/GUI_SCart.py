from tkinter import * 
#from tkinter.ttk import *
count=0
def add_to_cart():
	global count
	print(count)
	count+=1
	cart_label["text"]="CART("+str(count)+")"
	print(count)


window = Tk()
window.title("Shopping Cart Demo")
bttn1 = Button(window, text = "Add To Cart",command=add_to_cart)
#bttn1.bind("<Button-1>",add_to_cart)
bttn1.pack()
cart_txt="CART("+str(count)+")"
cart_label = Label(window, text =cart_txt)
cart_label.pack()
window.mainloop()