"""
The config() (or the identical configure()) method in Tkinter is used to modify the properties or options of a widget after it has been created. This allows for dynamic changes to the graphical user interface during runtime

"""

import tkinter as tk

root = tk.Tk()

def change_color_and_text():
    # Check current background and switch it
    if button['bg'] == 'red':
        button.config(bg='blue', fg='white', text='Clicked!')
    else:
        button.config(bg='red', fg='black', text='Click me')

# Create the button with initial properties
button = tk.Button(root, text='Click me', bg='red', fg='black', command=change_color_and_text)
button.pack(pady=10) # Position the button in the window

root.mainloop()