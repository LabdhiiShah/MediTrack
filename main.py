from tkinter import *
from frontend.modules import center

# import from frontend folder
from frontend.login import loginpage
from frontend.signup import signuppage
from frontend.dashboard import dashboardpage
from frontend.mymedicine import mymedicinepage
from frontend.reminder import reminderpage
from frontend.history import historypage

root = Tk()
root.title("MediTrack")
root.geometry("1100x700")
center(root, 1100, 700)

# container
container = Frame(root)
container.pack(fill="both", expand=True)

# imp, it expands frames and fill the container properly 
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

frames = {}

def show(page_name):
    frame = frames[page_name]
    if hasattr(frame, "refresh"):
        frame.refresh()
    frame.tkraise()

# register pages
pages = {
    # "string key" : "function to call"
    "login": loginpage,
    "signup": signuppage,
    "dashboard": dashboardpage,
    "mymedicine": mymedicinepage,
    "reminder": reminderpage,
    "history": historypage
    # "interactions":
    # "diet":
    # "profile":
}

# create frames
for name, func in pages.items():
    frame = func(container, show)
    frames[name] = frame
    frame.grid(row=0, column=0, sticky="nsew")

# start page
show("login")

root.mainloop()