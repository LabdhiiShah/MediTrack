from tkinter import *

# Create main window
window = Tk()
window.title("Login Form")
window.geometry("300x200")

# Title Label
lbl_title = Label(window, text="Login Form", font=("Arial", 14))
lbl_title.grid(row=0, column=0, columnspan=2, pady=10)

# Username Label and Entry
lbl_user = Label(window, text="Username")
lbl_user.grid(row=1, column=0, padx=10, pady=5)

txt_user = Entry(window)
txt_user.grid(row=1, column=1, padx=10, pady=5)

# Password Label and Entry
lbl_pass = Label(window, text="Password")
lbl_pass.grid(row=2, column=0, padx=10, pady=5)

txt_pass = Entry(window, show="*")
txt_pass.grid(row=2, column=1, padx=10, pady=5)

# Buttons
btn_login = Button(window, text="Login")
btn_login.grid(row=3, column=0, pady=10)

btn_cancel = Button(window, text="Reset")
btn_cancel.grid(row=3, column=1, pady=10)

# Run the window
window.mainloop()