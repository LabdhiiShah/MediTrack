import tkinter as tk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.title("Message Box Example")
root.geometry("200x100")

def show_info_box():
    root.withdraw()
    # Display the information message box
    messagebox.showinfo("Welcome", "This is an info box.")
    messagebox.showwarning("Welcome", "This is a warning box.")
    messagebox.showerror("Welcome", "This is an error box.")
    messagebox.askquestion("Welcome", "This is a question box.")
    messagebox.askokcancel("Welcome", "This is an ok/cancel box.")
    messagebox.askyesno("Welcome", "This is an ask yes/no box.")
    root.deiconify()

# Create a button that calls the show_info_box function when clicked
button = tk.Button(root, text="Click for Message", command=show_info_box)
button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()

