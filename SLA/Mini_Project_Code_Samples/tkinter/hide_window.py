import tkinter as tk

root = tk.Tk()
root.title("Main Window")

# Create a Toplevel window instance (but don't show it yet)
second_window = tk.Toplevel(root)
second_window.title("Second Window")
second_window.withdraw() # Start hidden

def open_second_window():
    second_window.deiconify() # Make the second window visible

def hide_second_window():
    second_window.withdraw() # Hide the second window

open_button = tk.Button(root, text="Open Second Window", command=open_second_window)
open_button.pack(pady=10)

hide_button_secondary = tk.Button(second_window, text="Hide Second Window", command=hide_second_window)
hide_button_secondary.pack(pady=10)

root.mainloop()
