import tkinter as tk

root = tk.Tk()
root.title("Sticky Example")

# Configure the grid to expand with the window
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a label and make it stick to all sides of its cell
label = tk.Label(root, text="I will stick and expand", bg="lightblue")
label.grid(row=0, column=0, sticky='nsew', padx=10, pady=10) #

root.mainloop()
