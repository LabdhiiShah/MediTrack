import tkinter as tk

root = tk.Tk()
root.title("Sticky Example")

tk.Label(root, text="Top").grid(row=0, column=0, sticky="N")
tk.Label(root, text="Bottom").grid(row=1, column=0, sticky="S")
tk.Label(root, text="Left").grid(row=2, column=0, sticky="W")
tk.Label(root, text="Right").grid(row=3, column=0, sticky="E")

tk.Button(root, text="Fill Cell").grid(row=4, column=0, sticky="NSEW")

root.mainloop()