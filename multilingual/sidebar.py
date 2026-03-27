from tkinter import *
from tkinter import ttk
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM
from i18n import i18n

def create_sidebar(parent, controller, active_page):

    sidebar = Frame(parent, width=220, bg=ACCENT)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # ── Logo Frame ────────────────────────────────────────────────────────────
    logoframe = Frame(sidebar, bg=ACCENT, pady=28)
    logoframe.pack(fill="x")

    logo = Canvas(logoframe, width=48, height=48, bg=ACCENT, highlightthickness=0)
    logo.pack()
    logo.create_oval(4, 4, 44, 44, fill="white", outline="")
    logo.create_text(24, 24, text="✚", font=FM(22, "bold"), fill=ACCENT)

    app_name_lbl = Label(logoframe, text=i18n.t("app_name"),
                         font=F(20, "bold"), bg=ACCENT, fg="white")
    app_name_lbl.pack()

    Frame(logoframe, height=1, bg="#236358").pack(fill="x", padx=4, pady=20)

    # ── Nav items (labels stored for refresh) ─────────────────────────────────
    nav_items = [
        ("🏠", "sidebar", "dashboard",      "dashboard"),
        ("💊", "sidebar", "my_medicines",   "mymedicine"),
        ("⏰", "sidebar", "reminders",      "reminder"),
        ("📋", "sidebar", "medical_history","history"),
        ("⚠️", "sidebar", "interactions",   "interactions"),
        ("🍎", "sidebar", "food_diet",      "diet"),
        ("👤", "sidebar", "profile",        "profile"),
    ]

    nav_text_labels = []   # (Label widget, section, key) for refresh

    def make_nav(icon, section, key, page):
        active = (i18n.t(section, key) == active_page or page == active_page.lower().replace(" ", ""))
        # match by page route for robustness
        is_active = (page == active_page) or (i18n.t(section, key) == active_page)

        frame = Frame(sidebar, bg=ACCENT if not is_active else "#236358", cursor="hand2")
        frame.pack(fill="x", padx=12, pady=2)

        if is_active:
            Frame(frame, bg=ACCENT2, width=2).pack(side="left", fill="y")

        inner = Frame(frame, bg=frame["bg"], padx=12, pady=10)
        inner.pack(side="left", fill="x", expand=True)

        Licon = Label(inner, text=icon, font=FM(14), bg=frame["bg"], fg="white")
        Licon.pack(side="left", padx=(0, 10))

        Ltext = Label(inner, text=i18n.t(section, key),
                      bg=frame["bg"],
                      font=FM(11, "bold" if is_active else "normal"),
                      fg="white" if is_active else "#A8D4CE")
        Ltext.pack(side="left")

        nav_text_labels.append((Ltext, section, key))

        def on_enter(e):
            frame.config(bg="#236358")
            inner.config(bg="#236358")
            Licon.config(bg="#236358")
            Ltext.config(bg="#236358")

        def on_leave(e):
            col = "#236358" if is_active else ACCENT
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

    for icon, section, key, page in nav_items:
        make_nav(icon, section, key, page)

    # ── Bottom divider ────────────────────────────────────────────────────────
    Frame(sidebar, bg="#236358", height=2).pack(fill="x", side="bottom", padx=20, pady=(0, 4))

    # ── Language Switcher ─────────────────────────────────────────────────────
    lang_frame = Frame(sidebar, bg=ACCENT)
    lang_frame.pack(side="bottom", fill="x", padx=16, pady=(0, 6))

    lang_lbl = Label(lang_frame, text=i18n.t("sidebar", "language"),
                     font=FM(9), bg=ACCENT, fg="#A8D4CE", anchor="w")
    lang_lbl.pack(fill="x")

    lang_map = {"English": "en", "हिंदी": "hi", "ગુજરાતી": "gu"}
    reverse_map = {v: k for k, v in lang_map.items()}

    lang_var = StringVar(value=reverse_map.get(i18n.lang, "English"))

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Lang.TCombobox",
                    fieldbackground="#236358",
                    background="#236358",
                    foreground="white",
                    selectbackground="#236358",
                    selectforeground="white")

    lang_menu = ttk.Combobox(lang_frame, textvariable=lang_var,
                              values=list(lang_map.keys()),
                              state="readonly", width=14,
                              style="Lang.TCombobox", font=FM(10))
    lang_menu.pack(fill="x", pady=(2, 0))

    def on_lang_change(e):
        chosen = lang_var.get()
        i18n.set_lang(lang_map[chosen])

    lang_menu.bind("<<ComboboxSelected>>", on_lang_change)

    # ── User card ─────────────────────────────────────────────────────────────
    userframe = Frame(sidebar, bg=ACCENT, pady=12)
    userframe.pack(side="bottom", fill="x")

    usercanva = Canvas(userframe, width=41, height=42, bg=ACCENT, highlightthickness=0)
    usercanva.pack()
    usercanva.create_oval(2, 2, 40, 40, fill=ACCENT2, outline="")
    usercanva.create_text(21, 21, text="L", font=FM(16, "bold"), fill="white")

    Label(userframe, text="Labdhi Shah", font=FM(10, "bold"),
          bg=ACCENT, fg="white").pack()

    # ── Refresh on language change ────────────────────────────────────────────
    def refresh():
        app_name_lbl.config(text=i18n.t("app_name"))
        lang_lbl.config(text=i18n.t("sidebar", "language"))
        for lbl, section, key in nav_text_labels:
            try:
                lbl.config(text=i18n.t(section, key))
            except Exception:
                pass

    i18n.on_change(refresh)

    return sidebar
