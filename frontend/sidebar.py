from tkinter import *
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM

def create_sidebar(parent, controller,active_page):

    sidebar = Frame(parent, width = 220, bg = ACCENT)
    sidebar.pack(side="left",fill="y")
    sidebar.pack_propagate(False)

    # FRAME FOR LOGO
    logoframe = Frame(sidebar,bg=ACCENT,pady=28)
    logoframe.pack(fill="x")

    logo = Canvas(logoframe,width=48, height=48, bg=ACCENT, highlightthickness=0)
    logo.pack()

    logo.create_oval(4, 4, 44, 44, fill="white", outline="")
    logo.create_text(24, 24, text="✚", font=FM(22, "bold"), fill=ACCENT)

    Label(logoframe,text="MediTrack",font=F(20,"bold"),bg=ACCENT,fg="white").pack()

    Frame(logoframe,height="1",bg="#236358").pack(fill="x",padx=4,pady=20)

    # ANOTHER FRAME FOR NAVIGATION

    nav_items = [
        ("🏠", "Dashboard",      "dashboard"),
        ("💊", "My Medicines",   "mymedicine"),
        ("⏰", "Reminders",      "reminder"),
        ("📋", "Medical History","history"),
        ("⚠️", "Interactions",   "interactions"),
        ("🍎", "Food & Diet",    "diet"),
        ("👤", "Profile",        "profile"),
    ]

    # nav_buttons = []

    def make_nav(icon, label, page):
        active = (label == active_page)
        frame = Frame(sidebar, bg=ACCENT if not active else "#236358", cursor="hand2")
        frame.pack(fill="x",padx=12,pady=2)

        if active:
            accent_bar = Frame(frame,bg=ACCENT2, width=2)
            accent_bar.pack(side="left",fill="y")

        inner = Frame(frame, bg=frame["bg"],padx=12,pady=10)
        inner.pack(side="left",fill="x",expand=True)

        Licon = Label(inner,text=icon,font=FM(14),bg=frame["bg"],fg="white")
        Licon.pack(side="left", padx=(0, 10))
        
        Ltext = Label(inner,text=label,
                    bg=frame["bg"],
                    font=FM(11, "bold" if active else "normal"),
                    fg="white" if active else "#A8D4CE")
        Ltext.pack(side="left")

        def on_enter(e):
            frame.config(bg="#236358")
            inner.config(bg="#236358")
            Licon.config(bg="#236358")
            Ltext.config(bg="#236358")

        def on_leave(e):
            col = "#236358" if active else ACCENT
            frame.config(bg=col)
            inner.config(bg=col)
            Licon.config(bg=col)
            Ltext.config(bg=col)

        def on_click(e):
            controller(page)

        for w in [frame, inner, Licon, Ltext]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)

        # pass

    for icon, label, page in nav_items:
        make_nav(icon, label, page)

    Frame(sidebar, bg="#236358", height=2).pack(fill="x",side="bottom",padx=20,pady=10)
    userframe = Frame(sidebar, bg=ACCENT, pady=16)
    userframe.pack(side="bottom",fill="x")

    usercanva = Canvas(userframe, width=41,height=42,bg=ACCENT,highlightthickness=0)
    usercanva.pack()
    usercanva.create_oval(2,2,40,40,fill=ACCENT2,outline="")
    usercanva.create_text(21,21,text="L",font=FM(16,"bold"),fill="white")
    
    Label(userframe,text="Labdhi Shah",font=FM(10,"bold"),bg=ACCENT,fg="white").pack()
    # Label(userframe,text="",font=FM(10,"bold"),bg=ACCENT,fg="white").pack()

    return sidebar