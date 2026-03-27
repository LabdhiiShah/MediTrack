import tkinter as tk

root = tk.Tk()
root.title("Tkinter Checkbutton")
root.geometry("210x80")

def show_state():
    print(var.get())
    checked = "Checked" if var.get() else "Unchecked"
    checkbox.config(text=f"Check me! ({checked})")

var = tk.IntVar()
print(var.get())
checkbox = tk.Checkbutton(root, text="Check me! (Checked)", variable=var)
checkbox.select()
checkbox.config(command=show_state)
checkbox.pack(padx=5, pady=10)

root.mainloop()