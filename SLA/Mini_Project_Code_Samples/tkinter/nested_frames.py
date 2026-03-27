import tkinter as tk

root = tk.Tk()
root.title("Nested Frames")
root.config(bg="skyblue")

frame = tk.Frame(root, width=200, height=200)
frame.pack(padx=10, pady=10)

nested_frame = tk.Frame(frame, width=190, height=190, bg="red")
nested_frame.pack(padx=10, pady=10)


nested_child_frame = tk.Frame(nested_frame, width=180, height=180, bg="yellow")
nested_child_frame.pack(padx=10, pady=10)

root.mainloop()