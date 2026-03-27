
#https://pythonassets.com/posts/browse-file-or-folder-in-tk-tkinter/
from tkinter import filedialog
from tkinter import *
root = Tk()
root.title("Main Window")
def browse():
    # for directory=> directory = filedialog.askdirectory()
    filename = filedialog.askopenfilename(
    parent=root,
    title="Browse File"
    )
    print(filename)

browsebtn = Button(
    master=root,
    text="BROWSE",
    command=browse
)
browsebtn.pack()
root.mainloop()