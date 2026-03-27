"""
MediTrack — main.py
Single Tk() root. All pages are Frames. No destroy/import tricks.
Pages: Login → Signup → Home (Dashboard, My Medicines, Reminders,
       Medical History, Interactions, Food & Diet, Profile)
Run:  python main.py
"""

import tkinter as tk
from tkinter import font as tkfont, filedialog, messagebox
from tkcalendar import DateEntry
import time

# ── Center helper ────────────────────────────────────────────────────────────
def center(win, w, h):
    win.update_idletasks()
    x = (win.winfo_screenwidth()  - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

# ── Palette ──────────────────────────────────────────────────────────────────
BG         = "#F5F0E8"
CARD       = "#FFFFFF"
ACCENT     = "#2D7D6F"
ACCENT2    = "#E8834A"
TEXT_DARK  = "#1A2B2A"
TEXT_MED   = "#4A6560"
TEXT_LIGHT = "#8FA8A3"
PILL_BG    = "#E6F4F1"
SECTION_BG = "#F0F7F5"
DANGER     = "#C0392B"
WARN       = "#E67E22"
SAFE       = "#27AE60"
NAV_ACTIVE = "#236358"

def F(size, weight="normal"):
    return tkfont.Font(family="Georgia", size=size, weight=weight)

def FM(size, weight="normal"):
    return tkfont.Font(family="Helvetica", size=size, weight=weight)

# ── Shared helpers ────────────────────────────────────────────────────────────
def scrollable(parent):
    """Returns (outer_frame, inner_frame). Pack content into inner_frame."""
    outer = tk.Frame(parent, bg=BG)
    cv    = tk.Canvas(outer, bg=BG, highlightthickness=0)
    vsb   = tk.Scrollbar(outer, orient="vertical", command=cv.yview)
    cv.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    cv.pack(side="left", fill="both", expand=True)
    inner = tk.Frame(cv, bg=BG)
    win   = cv.create_window((0, 0), window=inner, anchor="nw")
    inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
    cv.bind("<Configure>",    lambda e: cv.itemconfig(win, width=e.width))
    cv.bind_all("<MouseWheel>",
        lambda e: cv.yview_scroll(-1*(e.delta//120), "units"))
    return outer, inner

def page_header(parent, title, subtitle, btn_text=None, btn_cmd=None):
    hdr = tk.Frame(parent, bg=BG, padx=32, pady=24)
    hdr.pack(fill="x")
    lft = tk.Frame(hdr, bg=BG); lft.pack(side="left")
    tk.Label(lft, text=title,    font=F(22,"bold"), bg=BG, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(lft, text=subtitle, font=FM(11),       bg=BG, fg=TEXT_MED ).pack(anchor="w")
    if btn_text:
        b = tk.Label(hdr, text=btn_text, font=FM(10,"bold"),
                     bg=ACCENT, fg="white", padx=16, pady=8, cursor="hand2")
        b.pack(side="right", anchor="n")
        if btn_cmd: b.bind("<Button-1>", lambda e: btn_cmd())
        tk.Frame(parent, bg="#DDD8CC", height=1).pack(fill="x", padx=32)
        return b
    tk.Frame(parent, bg="#DDD8CC", height=1).pack(fill="x", padx=32)

def sec_hdr(parent, title, icon=""):
    f = tk.Frame(parent, bg=SECTION_BG, padx=20, pady=10)
    f.pack(fill="x", pady=(14, 0))
    tk.Label(f, text=f"{icon}  {title}" if icon else title,
             font=FM(12,"bold"), bg=SECTION_BG, fg=ACCENT).pack(anchor="w")

def card_frame(parent, padx=24, pady=16):
    c = tk.Frame(parent, bg=CARD, padx=padx, pady=pady)
    c.pack(fill="x", padx=32, pady=2)
    return c

def hdiv(parent):
    tk.Frame(parent, bg="#F0F0F0", height=1).pack(fill="x", pady=2)

def _darken(hex_color):
    r,g,b = int(hex_color[1:3],16),int(hex_color[3:5],16),int(hex_color[5:7],16)
    return f"#{max(0,r-30):02x}{max(0,g-30):02x}{max(0,b-30):02x}"

def action_btn(parent, text, color=ACCENT, cmd=None, side="left"):
    b = tk.Label(parent, text=text, font=FM(10,"bold"),
                 bg=color, fg="white", padx=14, pady=9, cursor="hand2")
    b.pack(side=side, padx=(0,8), pady=4)
    b.bind("<Enter>", lambda e: b.configure(bg=_darken(color)))
    b.bind("<Leave>", lambda e: b.configure(bg=color))
    if cmd: b.bind("<Button-1>", lambda e: cmd())
    return b

def styled_entry(parent, var=None, show="", width=28):
    if var is None: var = tk.StringVar()
    f = tk.Frame(parent, bg="#F5F5F5",
                 highlightthickness=1, highlightbackground="#DDD", highlightcolor=ACCENT)
    f.pack(fill="x", pady=(3,10))
    ent = tk.Entry(f, textvariable=var, font=FM(11), show=show,
                   relief="flat", bg="#F5F5F5", fg=TEXT_DARK, bd=0, width=width)
    ent.pack(side="left", fill="x", expand=True, ipady=7, padx=8)
    if show:
        eye = tk.Label(f, text="👁", font=FM(10), bg="#F5F5F5", cursor="hand2", padx=6)
        eye.pack(side="right")
        eye.bind("<Button-1>", lambda e: ent.config(show="" if ent.cget("show") else "*"))
    return var


# ════════════════════════════════════════════════════════════════════════════
#  APP
# ════════════════════════════════════════════════════════════════════════════
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MediTrack")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        center(self.root, 760, 520)

        self.container  = tk.Frame(self.root, bg=BG)
        self.container.pack(fill="both", expand=True)
        self.pages      = {}
        self.sub_pages  = {}
        self.nav_refs   = {}
        self.active_nav = "Dashboard"

        self._build_login()
        self._build_signup()
        self.show("login")
        self.root.mainloop()

    # ── Top-level page switcher ──────────────────────────────────────────────
    def show(self, name):
        if name == "home" and "home" not in self.pages:
            self._build_home()
        for p in self.pages.values():
            p.pack_forget()
        self.pages[name].pack(fill="both", expand=True)
        sizes = {"login":(760,520), "signup":(760,600), "home":(1100,720)}
        w, h  = sizes.get(name,(760,520))
        self.root.resizable(name=="home", name=="home")
        center(self.root, w, h)

    # ════════════════════════════════════════════════════════════════════════
    #  LOGIN
    # ════════════════════════════════════════════════════════════════════════
    def _build_login(self):
        page = tk.Frame(self.container, bg=BG)
        self.pages["login"] = page

        card = tk.Frame(page, bg=CARD, padx=52, pady=44)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        logo_row = tk.Frame(card, bg=CARD); logo_row.pack(pady=(0,28))
        cv = tk.Canvas(logo_row, width=40, height=40, bg=CARD, highlightthickness=0)
        cv.pack(side="left", padx=(0,10))
        cv.create_oval(2,2,38,38, fill=ACCENT, outline="")
        cv.create_text(20,20, text="✚", font=FM(16,"bold"), fill="white")
        tk.Label(logo_row, text="MediTrack", font=F(20,"bold"), bg=CARD, fg=ACCENT).pack(side="left")

        tk.Label(card, text="Welcome back",       font=F(15,"bold"), bg=CARD, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(card, text="Sign in to continue",font=FM(10),       bg=CARD, fg=TEXT_LIGHT).pack(anchor="w",pady=(2,20))

        tk.Label(card, text="Username", font=FM(10), bg=CARD, fg=TEXT_MED).pack(anchor="w")
        uvar = styled_entry(card)
        tk.Label(card, text="Password", font=FM(10), bg=CARD, fg=TEXT_MED).pack(anchor="w")
        pvar = styled_entry(card, show="*")

        err = tk.Label(card, text="", font=FM(9), bg=CARD, fg=DANGER)
        err.pack(anchor="w", pady=(0,6))

        def do_login():
            if not uvar.get().strip() or not pvar.get().strip():
                err.config(text="Please fill in all fields."); return
            err.config(text="")
            self.show("home")

        btn = tk.Label(card, text="Sign In", font=FM(12,"bold"),
                       bg=ACCENT, fg="white", cursor="hand2", pady=10)
        btn.pack(fill="x", pady=(4,16))
        btn.bind("<Button-1>", lambda e: do_login())
        btn.bind("<Enter>",    lambda e: btn.configure(bg=_darken(ACCENT)))
        btn.bind("<Leave>",    lambda e: btn.configure(bg=ACCENT))
        card.bind_all("<Return>", lambda e: do_login())

        tk.Frame(card, bg="#EEE", height=1).pack(fill="x", pady=4)
        row = tk.Frame(card, bg=CARD); row.pack(pady=(10,0))
        tk.Label(row, text="Don't have an account?", font=FM(10), bg=CARD, fg=TEXT_MED).pack(side="left")
        su = tk.Label(row, text="  Sign Up", font=FM(10,"bold"), bg=CARD, fg=ACCENT, cursor="hand2")
        su.pack(side="left")
        su.bind("<Button-1>", lambda e: self.show("signup"))

    # ════════════════════════════════════════════════════════════════════════
    #  SIGNUP
    # ════════════════════════════════════════════════════════════════════════
    def _build_signup(self):
        page = tk.Frame(self.container, bg=BG)
        self.pages["signup"] = page

        card = tk.Frame(page, bg=CARD, padx=52, pady=36)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="Create account",                     font=F(16,"bold"), bg=CARD, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(card, text="Fill in your details to get started",font=FM(10),       bg=CARD, fg=TEXT_LIGHT).pack(anchor="w",pady=(2,16))

        err = tk.Label(card, text="", font=FM(9), bg=CARD, fg=DANGER)
        err.pack(anchor="w")

        cols = tk.Frame(card, bg=CARD); cols.pack(fill="x")
        lc = tk.Frame(cols, bg=CARD); lc.pack(side="left", fill="x", expand=True, padx=(0,10))
        rc = tk.Frame(cols, bg=CARD); rc.pack(side="left", fill="x", expand=True)

        def col_entry(parent, label, show=""):
            tk.Label(parent, text=label, font=FM(10), bg=CARD, fg=TEXT_MED).pack(anchor="w")
            v = tk.StringVar()
            f = tk.Frame(parent, bg="#F5F5F5", highlightthickness=1,
                         highlightbackground="#DDD", highlightcolor=ACCENT)
            f.pack(fill="x", pady=(3,10))
            ent = tk.Entry(f, textvariable=v, font=FM(11), show=show,
                           relief="flat", bg="#F5F5F5", fg=TEXT_DARK, bd=0, width=20)
            ent.pack(side="left", fill="x", expand=True, ipady=7, padx=8)
            if show:
                eye = tk.Label(f, text="👁", font=FM(10), bg="#F5F5F5", cursor="hand2", padx=6)
                eye.pack(side="right")
                eye.bind("<Button-1>", lambda e: ent.config(show="" if ent.cget("show") else "*"))
            return v

        email_v   = col_entry(lc, "E-mail")
        user_v    = col_entry(rc, "Username")
        pw_v      = col_entry(lc, "Password",         show="*")
        cpw_v     = col_entry(rc, "Confirm Password", show="*")
        contact_v = col_entry(lc, "Contact (10 digits)")

        tk.Label(rc, text="Date of Birth", font=FM(10), bg=CARD, fg=TEXT_MED).pack(anchor="w")
        dob = DateEntry(rc, width=18, year=1970, font=FM(11),
                        background=ACCENT, foreground="white", borderwidth=0)
        dob.pack(fill="x", ipady=4, pady=(3,10))

        bot = tk.Frame(card, bg=CARD); bot.pack(fill="x", pady=(4,0))
        pic_lbl = tk.Label(bot, text="No file chosen", font=FM(9), bg=CARD, fg=TEXT_LIGHT)

        def upload():
            f = filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg")])
            if f: pic_lbl.config(text=f.split("/")[-1][:26], fg=TEXT_MED)

        action_btn(bot, "📷 Photo", color=TEXT_MED, cmd=upload)
        pic_lbl.pack(side="left", padx=6)

        disc_v = tk.IntVar()
        tk.Checkbutton(bot, text="Agree to disclaimer", variable=disc_v,
                       font=FM(9), bg=CARD, fg=TEXT_MED,
                       selectcolor=ACCENT, activebackground=CARD,
                       cursor="hand2").pack(side="right")

        def do_signup():
            e,u,p,cp,c = (email_v.get().strip(), user_v.get().strip(),
                           pw_v.get(), cpw_v.get(), contact_v.get().strip())
            if not all([e,u,p,cp,c]):
                err.config(text="All fields are required."); return
            if "@" not in e or "." not in e:
                err.config(text="Enter a valid email."); return
            if p != cp:
                err.config(text="Passwords do not match."); return
            if len(p) < 6:
                err.config(text="Password must be ≥ 6 characters."); return
            if not c.isdigit() or len(c) != 10:
                err.config(text="Contact must be exactly 10 digits."); return
            if not disc_v.get():
                err.config(text="Please accept the disclaimer."); return
            err.config(text="")
            self.show("login")

        sb = tk.Label(card, text="Create Account", font=FM(12,"bold"),
                      bg=ACCENT, fg="white", cursor="hand2", pady=10)
        sb.pack(fill="x", pady=(14,10))
        sb.bind("<Button-1>", lambda e: do_signup())
        sb.bind("<Enter>",    lambda e: sb.configure(bg=_darken(ACCENT)))
        sb.bind("<Leave>",    lambda e: sb.configure(bg=ACCENT))

        row = tk.Frame(card, bg=CARD); row.pack()
        tk.Label(row, text="Already have an account?", font=FM(10), bg=CARD, fg=TEXT_MED).pack(side="left")
        li = tk.Label(row, text="  Sign In", font=FM(10,"bold"), bg=CARD, fg=ACCENT, cursor="hand2")
        li.pack(side="left")
        li.bind("<Button-1>", lambda e: self.show("login"))

    # ════════════════════════════════════════════════════════════════════════
    #  HOME SHELL
    # ════════════════════════════════════════════════════════════════════════
    def _build_home(self):
        page = tk.Frame(self.container, bg=BG)
        self.pages["home"] = page

        # Sidebar
        sidebar = tk.Frame(page, bg=ACCENT, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        lf = tk.Frame(sidebar, bg=ACCENT, pady=22); lf.pack(fill="x")
        cv = tk.Canvas(lf, width=48, height=48, bg=ACCENT, highlightthickness=0); cv.pack()
        cv.create_oval(4,4,44,44, fill="white", outline="")
        cv.create_text(24,24, text="✚", font=FM(22,"bold"), fill=ACCENT)
        tk.Label(lf, text="MediTrack",           font=F(18,"bold"), bg=ACCENT, fg="white").pack()
        tk.Label(lf, text="Your health companion",font=FM(9),       bg=ACCENT, fg="#A8D4CE").pack()
        tk.Frame(sidebar, bg=NAV_ACTIVE, height=1).pack(fill="x", padx=20, pady=4)

        NAV = [("🏠","Dashboard"),("💊","My Medicines"),("⏰","Reminders"),
               ("📋","Medical History"),("⚠️","Interactions"),("🍎","Food & Diet"),("👤","Profile")]

        self.active_nav = "Dashboard"
        self.nav_refs   = {}

        def make_nav(icon, label):
            is_active = (label == self.active_nav)
            bg0 = NAV_ACTIVE if is_active else ACCENT
            frame = tk.Frame(sidebar, bg=bg0, cursor="hand2")
            frame.pack(fill="x", padx=12, pady=2)
            bar = tk.Frame(frame, bg=ACCENT2, width=4)
            bar.pack(side="left", fill="y")
            if not is_active: bar.pack_forget()
            lbl = tk.Label(frame, text=f"  {icon}  {label}",
                           font=FM(11,"bold" if is_active else "normal"),
                           bg=bg0, fg="white" if is_active else "#A8D4CE",
                           anchor="w", padx=8, pady=10)
            lbl.pack(side="left", fill="x", expand=True)
            self.nav_refs[label] = {"frame":frame,"bar":bar,"lbl":lbl}

            def set_bg(c):
                frame.configure(bg=c)
                for ch in frame.winfo_children():
                    try: ch.configure(bg=c)
                    except: pass

            def on_enter(e): set_bg(NAV_ACTIVE)
            def on_leave(e): set_bg(bg0)
            for w in [frame, bar, lbl]:
                w.bind("<Enter>",    on_enter)
                w.bind("<Leave>",    on_leave)
                w.bind("<Button-1>", lambda e, l=label: self.switch_nav(l))

        for icon, label in NAV:
            make_nav(icon, label)

        # User card
        tk.Frame(sidebar, bg=NAV_ACTIVE, height=1).pack(fill="x", side="bottom", padx=20, pady=6)
        uf = tk.Frame(sidebar, bg=ACCENT, pady=12); uf.pack(side="bottom", fill="x")
        av = tk.Canvas(uf, width=42, height=42, bg=ACCENT, highlightthickness=0); av.pack()
        av.create_oval(2,2,40,40, fill=ACCENT2, outline="")
        av.create_text(21,21, text="L", font=FM(16,"bold"), fill="white")
        tk.Label(uf, text="Labdhi Shah",      font=FM(10,"bold"), bg=ACCENT, fg="white").pack()
        tk.Label(uf, text="Patient · 22 yrs", font=FM(9),         bg=ACCENT, fg="#A8D4CE").pack()
        lo = tk.Label(uf, text="⏻  Logout", font=FM(9), bg=ACCENT,
                      fg="#A8D4CE", cursor="hand2", pady=4)
        lo.pack()
        lo.bind("<Button-1>", lambda e: self.show("login"))

        # Content area
        self.content_area = tk.Frame(page, bg=BG)
        self.content_area.pack(side="left", fill="both", expand=True)
        self.sub_pages = {}

        self._build_dashboard()
        self._build_medicines()
        self._build_reminders()
        self._build_medical_history()
        self._build_interactions()
        self._build_food_diet()
        self._build_profile()

        self._show_sub("Dashboard")

    def switch_nav(self, label):
        if label == self.active_nav: return
        old = self.nav_refs[self.active_nav]
        old["bar"].pack_forget()
        old["lbl"].configure(font=FM(11), fg="#A8D4CE")
        old["frame"].configure(bg=ACCENT); old["lbl"].configure(bg=ACCENT)
        self.active_nav = label
        new = self.nav_refs[label]
        new["frame"].configure(bg=NAV_ACTIVE)
        new["lbl"].configure(bg=NAV_ACTIVE, font=FM(11,"bold"), fg="white")
        new["bar"].pack(side="left", fill="y", before=new["lbl"])
        self._show_sub(label)

    def _show_sub(self, label):
        for sp in self.sub_pages.values(): sp.pack_forget()
        if label in self.sub_pages:
            self.sub_pages[label].pack(fill="both", expand=True)

    # ════════════════════════════════════════════════════════════════════════
    #  1. DASHBOARD
    # ════════════════════════════════════════════════════════════════════════
    def _build_dashboard(self):
        outer, inner = scrollable(self.content_area)
        self.sub_pages["Dashboard"] = outer

        tb = tk.Frame(inner, bg=BG, padx=30, pady=20); tb.pack(fill="x")
        lt = tk.Frame(tb, bg=BG); lt.pack(side="left")
        tk.Label(lt, text="Good morning, Labdhi 🌿",
                 font=F(20,"bold"), bg=BG, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(lt, text="Here's your health overview for today.",
                 font=FM(11), bg=BG, fg=TEXT_MED).pack(anchor="w")
        rt = tk.Frame(tb, bg=BG); rt.pack(side="right")
        clk = tk.Label(rt, text="", font=F(13,"bold"), bg=BG, fg=ACCENT); clk.pack(anchor="e")
        dat = tk.Label(rt, text="", font=FM(9),         bg=BG, fg=TEXT_LIGHT); dat.pack(anchor="e")
        def tick():
            now = time.localtime()
            clk.config(text=time.strftime("%I:%M %p", now))
            dat.config(text=time.strftime("%A, %d %B %Y", now))
            self.root.after(1000, tick)
        tick()

        sf = tk.Frame(inner, bg=BG, padx=30); sf.pack(fill="x", pady=(0,6))
        for i,(icon,title,val,col) in enumerate([
            ("💊","Active Medicines","5",None),("✅","Taken Today","3/5",SAFE),
            ("⚠️","Interactions","2",WARN),("📅","Days Left","12",ACCENT)
        ]):
            c = tk.Frame(sf, bg=CARD, padx=20, pady=14)
            c.grid(row=0, column=i, padx=8, pady=4, sticky="nsew")
            sf.columnconfigure(i, weight=1)
            tk.Label(c, text=icon,  font=FM(16), bg=CARD).pack(anchor="w")
            tk.Label(c, text=title, font=FM(9),  bg=CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=(4,0))
            tk.Label(c, text=val,   font=F(17,"bold"), bg=CARD, fg=col or TEXT_DARK).pack(anchor="w")

        cols = tk.Frame(inner, bg=BG, padx=22); cols.pack(fill="both", expand=True, pady=6)
        cols.columnconfigure(0,weight=3); cols.columnconfigure(1,weight=2)
        lc = tk.Frame(cols,bg=BG); lc.grid(row=0,column=0,sticky="nsew",padx=8)
        rc = tk.Frame(cols,bg=BG); rc.grid(row=0,column=1,sticky="nsew",padx=8)

        def shdr(p, t, btn_lbl=None, nav=None):
            r = tk.Frame(p, bg=BG); r.pack(fill="x", pady=(12,5))
            tk.Label(r, text=t, font=F(12,"bold"), bg=BG, fg=TEXT_DARK).pack(side="left")
            if btn_lbl and nav:
                b = tk.Label(r, text=btn_lbl, font=FM(10), bg=PILL_BG,
                             fg=ACCENT, padx=10, pady=3, cursor="hand2")
                b.pack(side="right")
                b.bind("<Button-1>", lambda e: self.switch_nav(nav))

        shdr(lc, "Today's Medicines", "+ Add Medicine", "My Medicines")
        for name,dose,timing,taken,tag in [
            ("Metformin 500mg","1 tablet","8:00 AM",True,"Diabetes"),
            ("Amlodipine 5mg","1 tablet","8:00 AM",True,"BP"),
            ("Vitamin D3","1 capsule","12:00 PM",False,"Supplement"),
            ("Aspirin 75mg","1 tablet","9:00 PM",False,"Heart"),
        ]:
            mc = tk.Frame(lc,bg=CARD,padx=14,pady=10); mc.pack(fill="x",pady=3)
            var = tk.BooleanVar(value=taken)
            lft = tk.Frame(mc,bg=CARD); lft.pack(side="left",fill="x",expand=True)
            top = tk.Frame(lft,bg=CARD); top.pack(anchor="w")
            tk.Checkbutton(top,variable=var,bg=CARD,activebackground=CARD,
                           selectcolor=ACCENT,relief="flat",cursor="hand2").pack(side="left")
            tk.Label(top,text=name,font=FM(10,"bold"),bg=CARD,
                     fg=TEXT_LIGHT if taken else TEXT_DARK).pack(side="left",padx=4)
            tk.Label(top,text=tag,font=FM(8),bg=PILL_BG,
                     fg=ACCENT,padx=5,pady=1).pack(side="left",padx=3)
            tk.Label(lft,text=f"{dose}  ·  {timing}",font=FM(9),
                     bg=CARD,fg=TEXT_LIGHT).pack(anchor="w")
            tk.Label(mc,text="✓ Taken" if taken else "⏳ Pending",
                     font=FM(9,"bold"),bg=CARD,
                     fg=SAFE if taken else WARN).pack(side="right")

        shdr(lc,"Interaction Alerts","View All","Interactions")
        for pair,desc,sev in [
            ("Metformin + Aspirin","Mild — increased bleeding risk.",WARN),
            ("Amlodipine + Atorvastatin","Moderate — monitor muscle pain.",DANGER),
        ]:
            ic = tk.Frame(lc,bg=CARD,padx=14,pady=10); ic.pack(fill="x",pady=3)
            tk.Frame(ic,bg=sev,width=4).pack(side="left",fill="y",padx=(0,10))
            inn = tk.Frame(ic,bg=CARD); inn.pack(side="left",fill="x",expand=True)
            tk.Label(inn,text=pair,font=FM(10,"bold"),bg=CARD,fg=TEXT_DARK).pack(anchor="w")
            tk.Label(inn,text=desc,font=FM(9),bg=CARD,fg=TEXT_MED,
                     wraplength=320,justify="left").pack(anchor="w")
            tk.Label(ic,text="⚠ Mild" if sev==WARN else "🔴 Mod",
                     font=FM(9,"bold"),bg=CARD,fg=sev).pack(side="right",anchor="n")

        shdr(rc,"Next Reminder")
        rem = tk.Frame(rc,bg=ACCENT,padx=16,pady=14); rem.pack(fill="x",pady=3)
        tk.Label(rem,text="💊 Vitamin D3",font=F(13,"bold"),bg=ACCENT,fg="white").pack(anchor="w")
        tk.Label(rem,text="1 capsule · 12:00 PM",font=FM(10),bg=ACCENT,fg="#A8D4CE").pack(anchor="w")
        tk.Frame(rem,bg=NAV_ACTIVE,height=1).pack(fill="x",pady=8)
        br = tk.Frame(rem,bg=ACCENT); br.pack(fill="x")
        tk.Label(br,text="🔔 WhatsApp set",font=FM(9),bg=ACCENT,fg="#A8D4CE").pack(side="left")
        tk.Label(br,text="In 1h 23m",font=FM(9,"bold"),bg=ACCENT,fg=ACCENT2).pack(side="right")

        shdr(rc,"Food Alerts")
        for icon,food,note in [
            ("🍊","Grapefruit","Avoid — Amlodipine"),
            ("🧀","Aged Cheese","Caution — BP meds"),
            ("🥗","Leafy Greens","Safe — Metformin"),
        ]:
            fc = tk.Frame(rc,bg=CARD,padx=12,pady=8); fc.pack(fill="x",pady=2)
            tk.Label(fc,text=icon,font=FM(14),bg=CARD).pack(side="left",padx=(0,8))
            inn = tk.Frame(fc,bg=CARD); inn.pack(side="left")
            tk.Label(inn,text=food,font=FM(10,"bold"),bg=CARD,fg=TEXT_DARK).pack(anchor="w")
            col = DANGER if "Avoid" in note else (WARN if "Caution" in note else SAFE)
            tk.Label(inn,text=note,font=FM(9),bg=CARD,fg=col).pack(anchor="w")

        shdr(rc,"Quick Actions")
        qa = tk.Frame(rc,bg=BG); qa.pack(fill="x",pady=(0,16))
        for i,(lbl,col) in enumerate([
            ("📷 Scan",ACCENT),("🎤 Voice",ACCENT2),
            ("📞 Caregiver",TEXT_MED),("📊 Report",TEXT_MED),
        ]):
            b = tk.Label(qa,text=lbl,font=FM(10,"bold"),bg=col,
                         fg="white",padx=8,pady=9,cursor="hand2")
            b.grid(row=i//2,column=i%2,padx=3,pady=3,sticky="ew")
            qa.columnconfigure(i%2,weight=1)
            b.bind("<Enter>",lambda e,btn=b,c=col: btn.configure(bg=_darken(c)))
            b.bind("<Leave>",lambda e,btn=b,c=col: btn.configure(bg=c))

        tk.Frame(inner,bg=BG,height=24).pack()

    # ════════════════════════════════════════════════════════════════════════
    #  2. MY MEDICINES
    # ════════════════════════════════════════════════════════════════════════
    def _build_medicines(self):
        outer, inner = scrollable(self.content_area)
        self.sub_pages["My Medicines"] = outer

        page_header(inner,"My Medicines","Manage your current prescriptions")

        sec_hdr(inner,"Add New Medicine","➕")
        form = card_frame(inner)

        def lbl_entry(parent, label, var, width=26):
            row = tk.Frame(parent,bg=CARD); row.pack(fill="x",pady=4)
            tk.Label(row,text=label,font=FM(10),bg=CARD,fg=TEXT_LIGHT,
                     width=18,anchor="w").pack(side="left")
            tk.Entry(row,textvariable=var,font=FM(11),width=width,relief="flat",
                     bg="#F5F5F5",highlightthickness=1,highlightbackground="#DDD",
                     highlightcolor=ACCENT).pack(side="left",ipady=6)
            return var

        name_v = tk.StringVar(); lbl_entry(form,"Medicine name",name_v)

        row2 = tk.Frame(form,bg=CARD); row2.pack(fill="x",pady=4)
        tk.Label(row2,text="Dosage",font=FM(10),bg=CARD,fg=TEXT_LIGHT,width=18,anchor="w").pack(side="left")
        dose_v = tk.StringVar(value="1")
        tk.Entry(row2,textvariable=dose_v,font=FM(11),width=5,relief="flat",
                 bg="#F5F5F5",highlightthickness=1,highlightbackground="#DDD",
                 highlightcolor=ACCENT).pack(side="left",ipady=6,padx=(0,6))
        unit_v = tk.StringVar(value="tablet")
        tk.OptionMenu(row2,unit_v,"tablet","capsule","ml","drops","mg").configure(
            font=FM(10),bg=CARD,relief="flat",cursor="hand2")
        tk.OptionMenu(row2,unit_v,"tablet","capsule","ml","drops","mg").pack(side="left",padx=(0,16))
        tk.Label(row2,text="Duration",font=FM(10),bg=CARD,fg=TEXT_LIGHT).pack(side="left")
        dur_v = tk.StringVar(value="7")
        tk.Entry(row2,textvariable=dur_v,font=FM(11),width=5,relief="flat",
                 bg="#F5F5F5",highlightthickness=1,highlightbackground="#DDD",
                 highlightcolor=ACCENT).pack(side="left",ipady=6,padx=6)
        tk.Label(row2,text="days",font=FM(10),bg=CARD,fg=TEXT_LIGHT).pack(side="left")

        row3 = tk.Frame(form,bg=CARD); row3.pack(fill="x",pady=4)
        tk.Label(row3,text="Schedule",font=FM(10),bg=CARD,fg=TEXT_LIGHT,width=18,anchor="w").pack(side="left")
        for slot in ["Morning","Afternoon","Evening","Night"]:
            v = tk.BooleanVar()
            tk.Checkbutton(row3,text=slot,variable=v,font=FM(10),bg=CARD,
                           activebackground=CARD,selectcolor=ACCENT,
                           cursor="hand2").pack(side="left",padx=6)

        cond_v = tk.StringVar(); lbl_entry(form,"Condition / tag",cond_v, width=22)

        btn_row = tk.Frame(form,bg=CARD); btn_row.pack(anchor="e",pady=(8,0))
        action_btn(btn_row,"💊  Add Medicine",
                   cmd=lambda: messagebox.showinfo("Added",
                       f"{name_v.get() or 'Medicine'} added successfully!"))

        sec_hdr(inner,"Current Medicines","💊")
        for name,dose,sched,dur,tag,active in [
            ("Metformin 500mg",  "1 tablet",  "Morning + Night","12 days","Diabetes",   True),
            ("Amlodipine 5mg",   "1 tablet",  "Morning",        "20 days","BP",         True),
            ("Vitamin D3",       "1 capsule", "Afternoon",      "30 days","Supplement", False),
            ("Atorvastatin 10mg","1 tablet",  "Night",          "15 days","Cholesterol",False),
            ("Aspirin 75mg",     "1 tablet",  "Night",          "10 days","Heart",      False),
        ]:
            mc = card_frame(inner,padx=20,pady=14)
            top = tk.Frame(mc,bg=CARD); top.pack(fill="x")
            lft = tk.Frame(top,bg=CARD); lft.pack(side="left",fill="x",expand=True)
            nr = tk.Frame(lft,bg=CARD); nr.pack(anchor="w")
            var = tk.BooleanVar(value=active)
            tk.Checkbutton(nr,variable=var,bg=CARD,activebackground=CARD,
                           selectcolor=ACCENT,relief="flat",cursor="hand2").pack(side="left")
            tk.Label(nr,text=name,font=FM(12,"bold"),bg=CARD,fg=TEXT_DARK).pack(side="left",padx=4)
            tk.Label(nr,text=tag,font=FM(8),bg=PILL_BG,fg=ACCENT,padx=6,pady=2).pack(side="left",padx=4)
            ir = tk.Frame(lft,bg=CARD); ir.pack(anchor="w")
            for t in [dose,sched,f"⏱ {dur}"]:
                tk.Label(ir,text=t,font=FM(9),bg=CARD,fg=TEXT_LIGHT).pack(side="left",padx=(0,12))
            rgt = tk.Frame(top,bg=CARD); rgt.pack(side="right",anchor="n")
            tk.Label(rgt,text="✓ Active" if active else "⏳ Pending",
                     font=FM(9,"bold"),bg=CARD,fg=SAFE if active else WARN).pack(anchor="e")
            dl = tk.Label(rgt,text="✕ Remove",font=FM(8),bg=CARD,fg=TEXT_LIGHT,cursor="hand2")
            dl.pack(anchor="e")
            dl.bind("<Button-1>",lambda e,f=mc: f.destroy())

        tk.Frame(inner,bg=BG,height=30).pack()

    # ════════════════════════════════════════════════════════════════════════
    #  3. REMINDERS
    # ════════════════════════════════════════════════════════════════════════
    def _build_reminders(self):
        outer, inner = scrollable(self.content_area)
        self.sub_pages["Reminders"] = outer

        page_header(inner,"Reminders","Never miss a dose")

        sec_hdr(inner,"Today's Schedule","📅")
        for time_str,meds,done in [
            ("8:00 AM", [("Metformin 500mg","1 tablet"),("Amlodipine 5mg","1 tablet")], True),
            ("12:00 PM",[("Vitamin D3","1 capsule")], False),
            ("9:00 PM", [("Aspirin 75mg","1 tablet"),("Atorvastatin 10mg","1 tablet")], False),
        ]:
            sc = card_frame(inner,padx=20,pady=14)
            hr = tk.Frame(sc,bg=CARD); hr.pack(fill="x")
            dot = tk.Canvas(hr,width=12,height=12,bg=CARD,highlightthickness=0)
            dot.pack(side="left",padx=(0,8))
            dot.create_oval(1,1,11,11,fill=SAFE if done else WARN,outline="")
            tk.Label(hr,text=time_str,font=FM(12,"bold"),bg=CARD,fg=TEXT_DARK).pack(side="left")
            tk.Label(hr,text="Completed" if done else "Upcoming",
                     font=FM(9),bg=CARD,fg=SAFE if done else WARN).pack(side="right")
            for m,d in meds:
                mr = tk.Frame(sc,bg=CARD); mr.pack(anchor="w",padx=20,pady=2)
                tk.Label(mr,text="💊",font=FM(11),bg=CARD).pack(side="left",padx=(0,6))
                tk.Label(mr,text=m,font=FM(10,"bold"),bg=CARD,fg=TEXT_DARK).pack(side="left")
                tk.Label(mr,text=f"  ·  {d}",font=FM(9),bg=CARD,fg=TEXT_LIGHT).pack(side="left")
                if not done:
                    v = tk.BooleanVar()
                    tk.Checkbutton(mr,variable=v,text="Mark taken",font=FM(9),
                                   bg=CARD,activebackground=CARD,selectcolor=SAFE,
                                   cursor="hand2").pack(side="right")

        sec_hdr(inner,"Notification Settings","🔔")
        ns = card_frame(inner)

        def toggle_row(parent, label, default=True):
            row = tk.Frame(parent,bg=CARD); row.pack(fill="x",pady=6)
            tk.Label(row,text=label,font=FM(10),bg=CARD,fg=TEXT_DARK).pack(side="left")
            v = tk.BooleanVar(value=default)
            tf = tk.Frame(row,bg=ACCENT if default else "#CCC",
                          width=44,height=24,cursor="hand2")
            tf.pack(side="right"); tf.pack_propagate(False)
            knob = tk.Frame(tf,bg="white",width=18,height=18)
            knob.place(x=22 if default else 2,y=3)
            def toggle(f=tf,k=knob,var=v):
                var.set(not var.get())
                f.configure(bg=ACCENT if var.get() else "#CCC")
                k.place(x=22 if var.get() else 2,y=3)
            tf.bind("<Button-1>",lambda e: toggle())
            knob.bind("<Button-1>",lambda e: toggle())
            return v

        toggle_row(ns,"🔔  Alarm / buzz on device")
        hdiv(ns)
        toggle_row(ns,"💬  WhatsApp message to self")
        hdiv(ns)
        toggle_row(ns,"📱  SMS to caregiver if missed",default=False)
        hdiv(ns)
        toggle_row(ns,"🔊  Speak medicine name aloud")
        hdiv(ns)
        toggle_row(ns,"📅  Auto-extend course on missed dose")

        row = tk.Frame(ns,bg=CARD); row.pack(fill="x",pady=(10,4))
        tk.Label(row,text="Caregiver number",font=FM(10),bg=CARD,
                 fg=TEXT_LIGHT,width=20,anchor="w").pack(side="left")
        cg_v = tk.StringVar(value="+91 98765 43210")
        tk.Entry(row,textvariable=cg_v,font=FM(11),width=22,relief="flat",
                 bg="#F5F5F5",highlightthickness=1,highlightbackground="#DDD",
                 highlightcolor=ACCENT).pack(side="left",ipady=6)

        br = tk.Frame(ns,bg=CARD); br.pack(anchor="e",pady=(8,0))
        action_btn(br,"💾  Save Settings",
                   cmd=lambda: messagebox.showinfo("Saved","Reminder settings saved."))

        tk.Frame(inner,bg=BG,height=30).pack()

    # ════════════════════════════════════════════════════════════════════════
    #  4. MEDICAL HISTORY
    # ════════════════════════════════════════════════════════════════════════
    def _build_medical_history(self):
        outer, inner = scrollable(self.content_area)
        self.sub_pages["Medical History"] = outer

        all_entries = []
        edit_state  = {"on": False}

        def toggle_edit():
            edit_state["on"] = not edit_state["on"]
            st = "normal" if edit_state["on"] else "disabled"
            for w in all_entries:
                try: w.configure(state=st)
                except: pass
            edit_btn.configure(
                text="💾  Save Changes" if edit_state["on"] else "✏️  Edit",
                bg=SAFE if edit_state["on"] else ACCENT)

        edit_btn = page_header(inner,"Medical History",
                               "Keep your health records accurate for better care",
                               btn_text="✏️  Edit",btn_cmd=toggle_edit)

        def field_row(parent, label, value="", is_text=False, h=2):
            row = tk.Frame(parent,bg=CARD); row.pack(fill="x",pady=4)
            tk.Label(row,text=label,font=FM(10),bg=CARD,
                     fg=TEXT_LIGHT,width=20,anchor="w").pack(side="left")
            if is_text:
                w = tk.Text(row,font=FM(10),fg=TEXT_DARK,bg="#F9F9F9",relief="flat",
                            height=h,width=34,wrap="word",state="disabled",
                            highlightthickness=1,highlightbackground="#E0E0E0",
                            highlightcolor=ACCENT)
                w.insert("1.0",value); w.pack(side="left",fill="x",expand=True)
                all_entries.append(w); return w
            else:
                v = tk.StringVar(value=value)
                e = tk.Entry(row,textvariable=v,font=FM(10),fg=TEXT_DARK,
                             bg="#F9F9F9",relief="flat",width=30,state="disabled",
                             highlightthickness=1,highlightbackground="#E0E0E0",
                             highlightcolor=ACCENT)
                e.pack(side="left",fill="x",expand=True)
                all_entries.append(e); return v

        def radio_row(parent,label,opts,default):
            row = tk.Frame(parent,bg=CARD,pady=4); row.pack(fill="x")
            tk.Label(row,text=label,font=FM(10),bg=CARD,
                     fg=TEXT_LIGHT,width=20,anchor="w").pack(side="left")
            v = tk.StringVar(value=default)
            for o in opts:
                tk.Radiobutton(row,text=o,variable=v,value=o,font=FM(10),
                               bg=CARD,selectcolor=ACCENT,activebackground=CARD,
                               cursor="hand2").pack(side="left",padx=6)

        sec_hdr(inner,"Personal Details","👤"); c = card_frame(inner)
        for lbl,val in [("Full Name","Labdhi Shah"),("Date of Birth","01/01/2002"),
                         ("Age","22 years"),("Gender","Female"),
                         ("Blood Group","B Positive"),("Height","162 cm"),
                         ("Weight","55 kg"),("BMI","20.9 (Normal)")]:
            field_row(c,lbl,val); hdiv(c)

        sec_hdr(inner,"Existing Conditions","🏥"); c2 = card_frame(inner)
        tk.Label(c2,text="Diagnosed conditions",font=FM(10),bg=CARD,fg=TEXT_LIGHT).pack(anchor="w")
        pr = tk.Frame(c2,bg=CARD); pr.pack(anchor="w",pady=4)
        for it in ["Type 2 Diabetes","Hypertension"]:
            p = tk.Frame(pr,bg=PILL_BG,padx=8,pady=3); p.pack(side="left",padx=(0,6))
            tk.Label(p,text=it,font=FM(9),bg=PILL_BG,fg=ACCENT).pack()
        hdiv(c2)
        field_row(c2,"Notes","Diabetes 2020. BP since 2022.",is_text=True)

        sec_hdr(inner,"Allergies","⚠️"); c3 = card_frame(inner)
        for lbl,items,col,bg in [
            ("Medicine",["Penicillin","Sulfa drugs"],DANGER,"#FDECEA"),
            ("Food",    ["Peanuts"],                  WARN,  "#FEF3E2"),
        ]:
            row = tk.Frame(c3,bg=CARD); row.pack(fill="x",pady=4)
            tk.Label(row,text=lbl,font=FM(10),bg=CARD,
                     fg=TEXT_LIGHT,width=20,anchor="w").pack(side="left")
            for it in items:
                p = tk.Frame(row,bg=bg,padx=8,pady=3); p.pack(side="left",padx=(0,5))
                tk.Label(p,text=it,font=FM(9),bg=bg,fg=col).pack()
            hdiv(c3)
        field_row(c3,"Environmental","Dust — seasonal",is_text=True,h=2)

        sec_hdr(inner,"Past Surgeries","🔬"); c4 = card_frame(inner)
        for proc,yr,hosp in [("Appendectomy","2015","City Hospital"),
                              ("Cataract (L)","2021","Eye Care Centre")]:
            row = tk.Frame(c4,bg=CARD,pady=5); row.pack(fill="x")
            lf = tk.Frame(row,bg=CARD); lf.pack(side="left",fill="x",expand=True)
            tk.Label(lf,text=proc,font=FM(11,"bold"),bg=CARD,fg=TEXT_DARK).pack(anchor="w")
            tk.Label(lf,text=f"{hosp}  ·  {yr}",font=FM(9),bg=CARD,fg=TEXT_LIGHT).pack(anchor="w")
            tk.Label(row,text="✓ Successful",font=FM(9,"bold"),bg=CARD,fg=SAFE).pack(side="right",anchor="n")
            hdiv(c4)

        sec_hdr(inner,"Lifestyle","🌿"); c5 = card_frame(inner)
        radio_row(c5,"Smoking",  ["Never","Former","Current"],"Never"); hdiv(c5)
        radio_row(c5,"Alcohol",  ["Never","Occasional","Regular"],"Never"); hdiv(c5)
        radio_row(c5,"Exercise", ["Sedentary","Light","Moderate","Active"],"Moderate"); hdiv(c5)
        radio_row(c5,"Diet",     ["Vegetarian","Non-Veg","Vegan"],"Vegetarian")

        sec_hdr(inner,"Last Recorded Vitals","📊"); c6 = card_frame(inner)
        for vname,val,status in [
            ("Blood Pressure","120/80 mmHg",SAFE),("Blood Sugar","108 mg/dL",SAFE),
            ("Cholesterol","168 mg/dL",SAFE),("HbA1c","6.8 %",WARN),
            ("Oxygen Sat","99 %",SAFE),("Pulse","72 bpm",SAFE),
        ]:
            row = tk.Frame(c6,bg=CARD,pady=5); row.pack(fill="x")
            tk.Label(row,text=vname,font=FM(10),bg=CARD,fg=TEXT_LIGHT,
                     width=22,anchor="w").pack(side="left")
            tk.Label(row,text=val,font=FM(11,"bold"),bg=CARD,fg=TEXT_DARK).pack(side="left")
            dot = tk.Canvas(row,width=10,height=10,bg=CARD,highlightthickness=0)
            dot.pack(side="right",padx=4); dot.create_oval(1,1,9,9,fill=status,outline="")
            hdiv(c6)

        sec_hdr(inner,"Caregiver & Emergency","📞"); c7 = card_frame(inner)
        for lbl,val in [("Caregiver name","Raj Shah"),("Relation","Brother"),
                         ("Phone","+91 98765 43210"),("Notify via","WhatsApp + SMS"),
                         ("Doctor","Dr. Priya Nair"),("Doctor contact","+91 80 4321 0000")]:
            field_row(c7,lbl,val); hdiv(c7)

        tk.Frame(inner,bg=BG,height=30).pack()

    # ════════════════════════════════════════════════════════════════════════
    #  5. INTERACTIONS
    # ════════════════════════════════════════════════════════════════════════
    def _build_interactions(self):
        outer, inner = scrollable(self.content_area)
        self.sub_pages["Interactions"] = outer

        page_header(inner,"Drug Interactions",
                    "Checked at add-time · results cached in your profile")

        sb = card_frame(inner,padx=20,pady=14)
        sbr = tk.Frame(sb,bg=CARD); sbr.pack(fill="x")
        for val,label,col in [("1","High risk",DANGER),("1","Moderate",WARN),("0","Mild",SAFE)]:
            b = tk.Frame(sbr,bg=CARD,padx=20,pady=6); b.pack(side="left")
            tk.Label(b,text=val,font=F(22,"bold"),bg=CARD,fg=col).pack()
            tk.Label(b,text=label,font=FM(9),bg=CARD,fg=TEXT_LIGHT).pack()
            tk.Frame(sbr,bg="#F0F0F0",width=1).pack(side="left",fill="y",padx=8)

        sec_hdr(inner,"Active Alerts","⚠️")
        for drug1,drug2,level,col,desc,rec in [
            ("Amlodipine","Atorvastatin","HIGH",DANGER,
             "Risk of myopathy and rhabdomyolysis. Muscle pain, weakness, or dark urine — seek care immediately.",
             "Avoid combination if possible. Monitor closely with lowest effective statin dose."),
            ("Metformin","Aspirin","MODERATE",WARN,
             "Aspirin may potentiate hypoglycaemic effect of metformin. Monitor blood sugar carefully.",
             "Check blood glucose more frequently. Dose adjustment may be needed."),
            ("Amlodipine","Aspirin","MILD",SAFE,
             "Additive blood-pressure-lowering effect. Generally well tolerated.",
             "Monitor BP. May actually be beneficial in some patients."),
        ]:
            ic = card_frame(inner,padx=0,pady=0)
            tk.Frame(ic,bg=col,width=6).pack(side="left",fill="y")
            body = tk.Frame(ic,bg=CARD,padx=18,pady=14); body.pack(side="left",fill="both",expand=True)
            top = tk.Frame(body,bg=CARD); top.pack(fill="x")
            tk.Label(top,text=f"{drug1}  ×  {drug2}",
                     font=FM(12,"bold"),bg=CARD,fg=TEXT_DARK).pack(side="left")
            sev_bg = {DANGER:"#FDECEA",WARN:"#FEF3E2",SAFE:"#EAF7EE"}[col]
            tk.Label(top,text=level,font=FM(8,"bold"),
                     bg=sev_bg,fg=col,padx=8,pady=3).pack(side="right")
            tk.Label(body,text=desc,font=FM(10),bg=CARD,fg=TEXT_MED,
                     wraplength=500,justify="left").pack(anchor="w",pady=(6,2))
            rf = tk.Frame(body,bg="#F9F9F9",padx=12,pady=8); rf.pack(fill="x",pady=(4,0))
            tk.Label(rf,text="💡 Recommendation",font=FM(9,"bold"),bg="#F9F9F9",fg=ACCENT).pack(anchor="w")
            tk.Label(rf,text=rec,font=FM(9),bg="#F9F9F9",fg=TEXT_MED,
                     wraplength=480,justify="left").pack(anchor="w")
            br = tk.Frame(body,bg=CARD); br.pack(anchor="w",pady=(8,0))
            action_btn(br,"✨ Explain simply",
                       cmd=lambda d=desc: messagebox.showinfo("Explanation",d))
            action_btn(br,"📋 Copy",color=TEXT_MED,
                       cmd=lambda d=f"{drug1} × {drug2}: {desc}":
                           (self.root.clipboard_clear(),self.root.clipboard_append(d)))

        sec_hdr(inner,"Check a Pair Manually","🔍")
        mc = card_frame(inner)
        mrow = tk.Frame(mc,bg=CARD); mrow.pack(fill="x",pady=4)
        tk.Label(mrow,text="Drug A",font=FM(10),bg=CARD,fg=TEXT_LIGHT,width=8,anchor="w").pack(side="left")
        a_v = tk.StringVar()
        tk.Entry(mrow,textvariable=a_v,font=FM(11),width=18,relief="flat",
                 bg="#F5F5F5",highlightthickness=1,highlightbackground="#DDD",
                 highlightcolor=ACCENT).pack(side="left",ipady=6,padx=(0,16))
        tk.Label(mrow,text="Drug B",font=FM(10),bg=CARD,fg=TEXT_LIGHT).pack(side="left")
        b_v = tk.StringVar()
        tk.Entry(mrow,textvariable=b_v,font=FM(11),width=18,relief="flat",
                 bg="#F5F5F5",highlightthickness=1,highlightbackground="#DDD",
                 highlightcolor=ACCENT).pack(side="left",ipady=6,padx=(8,0))
        br2 = tk.Frame(mc,bg=CARD); br2.pack(anchor="w",pady=(8,0))
        action_btn(br2,"🔍 Check Interaction",
                   cmd=lambda: messagebox.showinfo("Check",
                       f"Checking: {a_v.get()} × {b_v.get()}\n(API call goes here)"))

        tk.Frame(inner,bg=BG,height=30).pack()

    # ════════════════════════════════════════════════════════════════════════
    #  6. FOOD & DIET
    # ════════════════════════════════════════════════════════════════════════
    def _build_food_diet(self):
        outer, inner = scrollable(self.content_area)
        self.sub_pages["Food & Diet"] = outer

        page_header(inner,"Food & Diet Guide",
                    "Based on your medicines and medical history")

        sec_hdr(inner,"Foods to Avoid","🚫")
        for icon,food,reason,med in [
            ("🍊","Grapefruit / citrus juice","Increases Amlodipine concentration dangerously","Amlodipine"),
            ("🧀","Aged cheeses & cured meats","Tyramine interaction — BP spike risk","BP medicines"),
            ("🍺","Alcohol","Enhances hypoglycaemic effect of Metformin","Metformin"),
        ]:
            fc = card_frame(inner,padx=0,pady=0)
            tk.Frame(fc,bg=DANGER,width=6).pack(side="left",fill="y")
            body = tk.Frame(fc,bg=CARD,padx=18,pady=14); body.pack(side="left",fill="both",expand=True)
            top = tk.Frame(body,bg=CARD); top.pack(fill="x")
            tk.Label(top,text=f"{icon}  {food}",font=FM(12,"bold"),
                     bg=CARD,fg=TEXT_DARK).pack(side="left")
            tk.Label(top,text=f"Reacts with {med}",font=FM(8),
                     bg="#FDECEA",fg=DANGER,padx=8,pady=3).pack(side="right")
            tk.Label(body,text=reason,font=FM(10),bg=CARD,fg=TEXT_MED,wraplength=500).pack(anchor="w",pady=(4,0))

        sec_hdr(inner,"Consume with Caution","⚠️")
        for icon,food,note in [
            ("🥦","High-potassium foods (banana, spinach)","Monitor with ACE inhibitors"),
            ("🥛","Dairy — large amounts","May slow absorption of some medicines"),
            ("☕","Caffeine","May affect blood pressure readings"),
        ]:
            fc = card_frame(inner,padx=0,pady=0)
            tk.Frame(fc,bg=WARN,width=6).pack(side="left",fill="y")
            body = tk.Frame(fc,bg=CARD,padx=18,pady=12); body.pack(side="left",fill="both",expand=True)
            tk.Label(body,text=f"{icon}  {food}",font=FM(11,"bold"),bg=CARD,fg=TEXT_DARK).pack(anchor="w")
            tk.Label(body,text=note,font=FM(9),bg=CARD,fg=TEXT_MED).pack(anchor="w",pady=(3,0))

        sec_hdr(inner,"Recommended Foods","✅")
        grid = tk.Frame(inner,bg=BG,padx=32); grid.pack(fill="x",pady=6)
        for i,(icon,food,note) in enumerate([
            ("🥗","Leafy greens","Safe with all current meds"),
            ("🐟","Fatty fish","Omega-3 supports heart health"),
            ("🫐","Berries","Antioxidants — no interactions"),
            ("🌾","Whole grains","Supports Metformin effectiveness"),
        ]):
            fc = tk.Frame(grid,bg=CARD,padx=14,pady=12)
            fc.grid(row=i//2,column=i%2,padx=6,pady=6,sticky="nsew")
            grid.columnconfigure(i%2,weight=1)
            tk.Label(fc,text=f"{icon}  {food}",font=FM(11,"bold"),bg=CARD,fg=TEXT_DARK).pack(anchor="w")
            tk.Label(fc,text=note,font=FM(9),bg=CARD,fg=SAFE).pack(anchor="w")

        sec_hdr(inner,"Your Allergy Flags","🏷️")
        af = card_frame(inner)
        tr = tk.Frame(af,bg=CARD); tr.pack(anchor="w",pady=4)
        for a in ["Penicillin","Sulfa drugs","Peanuts"]:
            p = tk.Frame(tr,bg="#FDECEA",padx=10,pady=4); p.pack(side="left",padx=(0,8))
            tk.Label(p,text=f"⚠ {a}",font=FM(9,"bold"),bg="#FDECEA",fg=DANGER).pack()
        hdiv(af)
        ar = tk.Frame(af,bg=CARD); ar.pack(fill="x",pady=(8,0))
        tk.Label(ar,text="Ask about a food:",font=FM(10),bg=CARD,
                 fg=TEXT_LIGHT,width=18,anchor="w").pack(side="left")
        ask_v = tk.StringVar()
        tk.Entry(ar,textvariable=ask_v,font=FM(11),width=24,relief="flat",
                 bg="#F5F5F5",highlightthickness=1,highlightbackground="#DDD",
                 highlightcolor=ACCENT).pack(side="left",ipady=6,padx=(0,8))
        action_btn(ar,"✨ Ask AI",
                   cmd=lambda: messagebox.showinfo("AI Response",
                       f"Checking '{ask_v.get()}' against your profile…\n(LLM call goes here)"))

        tk.Frame(inner,bg=BG,height=30).pack()

    # ════════════════════════════════════════════════════════════════════════
    #  7. PROFILE
    # ════════════════════════════════════════════════════════════════════════
    def _build_profile(self):
        outer, inner = scrollable(self.content_area)
        self.sub_pages["Profile"] = outer

        page_header(inner,"Profile & Settings","Manage your account preferences")

        sec_hdr(inner,"Account","👤")
        ac = card_frame(inner)
        arow = tk.Frame(ac,bg=CARD); arow.pack(fill="x",pady=8)
        av = tk.Canvas(arow,width=64,height=64,bg=CARD,highlightthickness=0)
        av.pack(side="left",padx=(0,16))
        av.create_oval(2,2,62,62,fill=ACCENT2,outline="")
        av.create_text(32,32,text="L",font=FM(26,"bold"),fill="white")
        info = tk.Frame(arow,bg=CARD); info.pack(side="left")
        tk.Label(info,text="Labdhi Shah",      font=F(16,"bold"),bg=CARD,fg=TEXT_DARK).pack(anchor="w")
        tk.Label(info,text="labdhi@email.com", font=FM(10),      bg=CARD,fg=TEXT_MED ).pack(anchor="w")
        tk.Label(info,text="Patient · 22 yrs · B+",font=FM(9),  bg=CARD,fg=TEXT_LIGHT).pack(anchor="w")
        action_btn(arow,"📷 Change Photo",color=TEXT_MED,
                   cmd=lambda: filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg")]))
        hdiv(ac)
        for lbl,val in [("Full Name","Labdhi Shah"),("Email","labdhi@email.com"),
                         ("Contact","+91 98765 43210")]:
            row = tk.Frame(ac,bg=CARD); row.pack(fill="x",pady=4)
            tk.Label(row,text=lbl,font=FM(10),bg=CARD,fg=TEXT_LIGHT,
                     width=16,anchor="w").pack(side="left")
            v = tk.StringVar(value=val)
            tk.Entry(row,textvariable=v,font=FM(11),width=26,relief="flat",
                     bg="#F5F5F5",highlightthickness=1,highlightbackground="#DDD",
                     highlightcolor=ACCENT).pack(side="left",ipady=6)
        br = tk.Frame(ac,bg=CARD); br.pack(anchor="e",pady=(8,0))
        action_btn(br,"💾  Save Profile",
                   cmd=lambda: messagebox.showinfo("Saved","Profile updated."))

        sec_hdr(inner,"Notification Preferences","🔔")
        nc = card_frame(inner)
        for label,default in [
            ("Reminder alarm on device",True),
            ("WhatsApp notifications",True),
            ("SMS to caregiver",False),
            ("Missed dose alerts",True),
            ("Weekly adherence report",False),
        ]:
            row = tk.Frame(nc,bg=CARD); row.pack(fill="x",pady=5)
            tk.Label(row,text=label,font=FM(10),bg=CARD,fg=TEXT_DARK).pack(side="left")
            v = tk.BooleanVar(value=default)
            tk.Checkbutton(row,variable=v,bg=CARD,activebackground=CARD,
                           selectcolor=ACCENT,cursor="hand2").pack(side="right")
            hdiv(nc)

        sec_hdr(inner,"Language & Accessibility","🌐")
        lc = card_frame(inner)
        lr = tk.Frame(lc,bg=CARD); lr.pack(fill="x",pady=4)
        tk.Label(lr,text="Language",font=FM(10),bg=CARD,
                 fg=TEXT_LIGHT,width=16,anchor="w").pack(side="left")
        lang_v = tk.StringVar(value="English")
        dd = tk.OptionMenu(lr,lang_v,"English","हिंदी","मराठी","ગુજરાતી","தமிழ்","తెలుగు")
        dd.configure(font=FM(10),bg=CARD,relief="flat",cursor="hand2"); dd.pack(side="left")
        hdiv(lc)
        fr = tk.Frame(lc,bg=CARD); fr.pack(fill="x",pady=4)
        tk.Label(fr,text="Font size",font=FM(10),bg=CARD,
                 fg=TEXT_LIGHT,width=16,anchor="w").pack(side="left")
        fs_v = tk.StringVar(value="Medium")
        for opt in ["Small","Medium","Large","Extra Large"]:
            tk.Radiobutton(fr,text=opt,variable=fs_v,value=opt,font=FM(10),
                           bg=CARD,selectcolor=ACCENT,activebackground=CARD,
                           cursor="hand2").pack(side="left",padx=8)

        sec_hdr(inner,"Security","🔒")
        sc = card_frame(inner)
        for lbl in ["Current password","New password","Confirm new password"]:
            row = tk.Frame(sc,bg=CARD); row.pack(fill="x",pady=4)
            tk.Label(row,text=lbl,font=FM(10),bg=CARD,fg=TEXT_LIGHT,
                     width=20,anchor="w").pack(side="left")
            v = tk.StringVar()
            f = tk.Frame(row,bg="#F5F5F5",highlightthickness=1,
                         highlightbackground="#DDD",highlightcolor=ACCENT)
            f.pack(side="left")
            ent = tk.Entry(f,textvariable=v,font=FM(11),show="*",relief="flat",
                           bg="#F5F5F5",bd=0,width=22)
            ent.pack(ipady=6,padx=8)
        br2 = tk.Frame(sc,bg=CARD); br2.pack(anchor="e",pady=(8,0))
        action_btn(br2,"🔒 Update Password",
                   cmd=lambda: messagebox.showinfo("Updated","Password changed."))

        sec_hdr(inner,"Danger Zone","⛔")
        dz = card_frame(inner)
        drow = tk.Frame(dz,bg=CARD); drow.pack(fill="x")
        tk.Label(drow,text="Delete all data and account permanently.",
                 font=FM(10),bg=CARD,fg=TEXT_MED).pack(side="left")
        action_btn(drow,"🗑  Delete Account",color=DANGER,
                   cmd=lambda: messagebox.askyesno("Confirm",
                       "Are you sure? This cannot be undone."))
        lo_row = tk.Frame(dz,bg=CARD); lo_row.pack(fill="x",pady=(8,0))
        action_btn(lo_row,"⏻  Logout",color=TEXT_MED,
                   cmd=lambda: self.show("login"))

        tk.Frame(inner,bg=BG,height=30).pack()


# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    App()