from tkinter import *

# Create main window
window = Tk()
window.title("Tkinter Geometry Managers Example")
window.geometry("500x400")

# ---------------- PACK MANAGER ----------------
frame_pack = Frame(window, bg="lightblue", bd=2, relief="solid")
frame_pack.pack(side=TOP, fill=X, padx=10, pady=10)

Label(frame_pack, text="PACK Manager Example", bg="lightblue").pack()

Button(frame_pack, text="Button 1").pack(side=LEFT, padx=5, pady=5)
Button(frame_pack, text="Button 2").pack(side=LEFT, padx=5, pady=5)
Button(frame_pack, text="Button 3").pack(side=LEFT, padx=5, pady=5)

# ---------------- GRID MANAGER ----------------
frame_grid = Frame(window, bg="lightgreen", bd=2, relief="solid")
frame_grid.pack(fill=X, padx=10, pady=10)

Label(frame_grid, text="GRID Manager Example", bg="lightgreen").grid(row=0, column=0, columnspan=2)

Label(frame_grid, text="Username").grid(row=1, column=0, padx=5, pady=5)
Entry(frame_grid).grid(row=1, column=1, padx=5, pady=5)

Label(frame_grid, text="Password").grid(row=2, column=0, padx=5, pady=5)
Entry(frame_grid).grid(row=2, column=1, padx=5, pady=5)

Button(frame_grid, text="Login").grid(row=3, column=0, columnspan=2, pady=5)

# ---------------- PLACE MANAGER ----------------
frame_place = Frame(window, bg="lightyellow", bd=2, relief="solid", height=120)
frame_place.pack(fill=BOTH, padx=10, pady=10)

Label(frame_place, text="PLACE Manager Example", bg="lightyellow").place(x=10, y=10)

Button(frame_place, text="Button A").place(x=50, y=40)
Button(frame_place, text="Button B").place(x=150, y=40)
Button(frame_place, text="Button C").place(x=250, y=40)

# Run the window
window.mainloop()