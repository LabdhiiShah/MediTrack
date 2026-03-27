import tkinter as tk
from itertools import cycle
from PIL import Image,ImageTk
#from ImageTk import PhotoImage

images = ["bird.jpeg", "bird1.jpeg", "bird3.jpeg", "bird4.jpeg"]
photos = cycle(ImageTk.PhotoImage(file=image) for image in images)

def slideShow():
  img = next(photos)
  displayCanvas.config(image=img)
  root.after(1000, slideShow) # 0.05 seconds

root = tk.Tk()
root.overrideredirect(True)
width = root.winfo_screenwidth()
height = root.winfo_screenwidth()
root.geometry('%dx%d' % (640, 480))
displayCanvas = tk.Label(root)
displayCanvas.pack()
root.after(10, lambda: slideShow())
root.mainloop()