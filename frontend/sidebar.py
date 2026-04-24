import os
from tkinter import *
from PIL import Image, ImageTk, ImageOps, ImageDraw 
from backend.db import getConnection
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM
#from frontend.translation import LANGUAGES
from frontend import session

def create_sidebar(parent, controller, active_page):
   # texts = LANGUAGES.get(session.language, LANGUAGES["English"])
    frame = Frame(parent, width=220, bg=ACCENT)
    frame.pack(side="left", fill="y")
    frame.pack_propagate(False)

    # ── Logo ──────────────────────────────────────────────────────────────────
    logoframe = Frame(frame, bg=ACCENT, pady=28)
    logoframe.pack(fill="x")

    logo = Canvas(logoframe, width=48, height=48, bg=ACCENT, highlightthickness=0)
    logo.pack()
    logo.create_oval(4, 4, 44, 44, fill="white", outline="")
    logo.create_text(24, 24, text="✚", font=FM(22, "bold"), fill=ACCENT)

    Label(logoframe, text="MediTrack", font=F(20, "bold"), bg=ACCENT, fg="white").pack()
    Frame(logoframe, height=1, bg="#236358").pack(fill="x", padx=4, pady=20)

    # Navigation items mapped to translation keys and page IDs
    nav_items = [
            ("🏠", "Dashboard",      "dashboard"),
            ("💊", "My Medicines",   "mymedicine"),
            ("⏰", "Reminders",      "reminder"),
            ("📋", "Medical History","history"),
            ("⚠️", "Interactions",   "interaction"),
            ("🍎", "Food & Diet",    "diet"),
            ("👤", "Profile",        "profile"),
        ]


    def make_nav(icon, label, page):
        # We check against page ID to keep active state consistent
        active = (page == active_page)

        nav_box = Frame(frame, bg=ACCENT if not active else "#236358", cursor="hand2")
        nav_box.pack(fill="x", padx=12, pady=2)

        if active:
            Frame(nav_box, bg=ACCENT2, width=2).pack(side="left", fill="y")

        inner = Frame(nav_box, bg=nav_box["bg"], padx=12, pady=10)
        inner.pack(side="left", fill="x", expand=True)

        Licon = Label(inner, text=icon, font=FM(14), bg=nav_box["bg"], fg="white")
        Licon.pack(side="left", padx=(0, 10))

        Ltext = Label(inner, text=label, bg=nav_box["bg"],
                      font=FM(11, "bold" if active else "normal"),
                      fg="white" if active else "#A8D4CE")
        Ltext.pack(side="left")

        def on_enter(e):
            for w in [nav_box, inner, Licon, Ltext]:
                w.config(bg="#236358")

        def on_leave(e):
            col = "#236358" if active else ACCENT
            for w in [nav_box, inner, Licon, Ltext]:
                w.config(bg=col)

        for w in [nav_box, inner, Licon, Ltext]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", lambda e, p=page: controller(p))

    for icon, label, page in nav_items:
        make_nav(icon, label, page)

    # ── User Profile Section ──────────────────────────────────────────────────
    userframe = Frame(frame, bg=ACCENT, pady=16)
    userframe.pack(side="bottom", fill="x")

    profile_pic = Label(userframe, bg=ACCENT)
    
    usercanva = Canvas(userframe, width=41, height=42, bg=ACCENT, highlightthickness=0)
    avatar_oval = usercanva.create_oval(2, 2, 40, 40, fill=ACCENT2, outline="")
    avatar_text = usercanva.create_text(21, 21, text="", font=FM(14, "bold"), fill="white")

    username_label = Label(userframe, text="", font=FM(10, "bold"), bg=ACCENT, fg="white")
    username_label.pack()

    def getid():
        pid = session.patientid
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_img_path = os.path.join(base_dir, "profile.png")

        if pid is None:
            username_label.config(text="")
            profile_pic.pack_forget()
            usercanva.pack_forget()
            return

        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username, profile FROM patientinfo WHERE id = %s", (pid,))
            data = cursor.fetchone()
            
            if data:
                name = data['username']
                username_label.config(text=name)
                
                profile_path = data.get('profile')
                img_to_use = profile_path if profile_path and os.path.exists(profile_path) else default_img_path

                if os.path.exists(img_to_use):
                    usercanva.pack_forget()
                    try:
                        img = Image.open(img_to_use).convert("RGBA")
                        size = (40, 40)
                        img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
                        mask = Image.new('L', size, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0, 0) + size, fill=255)
                        output = Image.new('RGBA', size, (0, 0, 0, 0))
                        output.paste(img, (0, 0), mask=mask)

                        photo = ImageTk.PhotoImage(output)
                        profile_pic.config(image=photo)
                        profile_pic.image = photo 
                        profile_pic.pack(before=username_label, pady=(0, 5))
                    except:
                        profile_pic.pack_forget()
                        usercanva.itemconfig(avatar_text, text=name[0].upper())
                        usercanva.pack(before=username_label)
                else:
                    profile_pic.pack_forget()
                    usercanva.itemconfig(avatar_text, text=name[0].upper())
                    usercanva.pack(before=username_label)
            conn.close()
        except Exception as e:
            print(f"[sidebar] getid error: {e}")

    def logout(e):
        session.patientid = None
        controller("login")

    logoutlbl = Label(userframe, text = "Log Out", font=FM(10, "bold"),
                      bg=ACCENT, fg="white", cursor="hand2")
    logoutlbl.pack()
    logoutlbl.bind("<Button-1>", logout)

    # Initial load of user info
    getid()
    
    frame.refresh = getid
    return frame