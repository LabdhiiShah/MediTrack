import tkinter as tk

def open_toplevel_window():
    # Create a new Toplevel window
    new_window = tk.Toplevel(root)
    new_window.title("New Window")
    new_window.geometry("200x100")

    # Add a label to the new window
    tk.Label(new_window, text="This is a Toplevel window!").pack(pady=10)

    # Add a button to close the new window
    tk.Button(new_window, text="Close", command=new_window.destroy).pack(pady=5)

# Main application window
root = tk.Tk()
root.title("Main Window")
root.geometry("300x200")

# Button in the main window to open the Toplevel window
open_button = tk.Button(root, text="Open Toplevel Window", command=open_toplevel_window)
open_button.pack(pady=80)

# Start the Tkinter event loop
root.mainloop()
