from tkinter import *
from frontend.sidebar import create_sidebar
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM

def dashboardpage(parent, controller):
    frame = Frame(parent, bg=BG)

    container = Frame(frame)
    container.pack(fill="both",expand=True)

    create_sidebar(container, controller, active_page = "Dashboard")

    main = Frame(container)
    main.pack(expand="true",fill="both")
        
    # Main Frame
    content = scrollablefunc(main,BG)

    return frame
        