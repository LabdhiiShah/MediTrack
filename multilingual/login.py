from tkinter import *
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM
from i18n import i18n

def loginpage(parent, controller):
    frame = Frame(parent, bg=BG)

    card = Frame(frame, bg=CARD, padx=36, pady=32, relief="flat", bd=0)
    card.place(relx=0.5, rely=0.5, anchor=CENTER)

    # ── Logo ──────────────────────────────────────────────────────────────────
    logo_canvas = Canvas(card, width=44, height=44, bg=CARD, highlightthickness=0)
    logo_canvas.grid(row=0, column=0, columnspan=2, pady=(0, 4))
    logo_canvas.create_oval(2, 2, 42, 42, fill=ACCENT, outline="")
    logo_canvas.create_text(22, 22, text="✚", font=FM(16, "bold"), fill="white")

    app_lbl = Label(card, text=i18n.t("app_name"), font=F(15, "bold"),
                    bg=CARD, fg=TEXT_DARK)
    app_lbl.grid(row=1, column=0, columnspan=2)

    subtitle_lbl = Label(card, text=i18n.t("login", "subtitle"), font=FM(9),
                         bg=CARD, fg=TEXT_LIGHT)
    subtitle_lbl.grid(row=2, column=0, columnspan=2, pady=(2, 16))

    # ── Username ──────────────────────────────────────────────────────────────
    username_lbl = Label(card, text=i18n.t("login", "username"), font=FM(9),
                         bg=CARD, anchor="w")
    username_lbl.grid(row=3, column=0, columnspan=2, sticky="w", padx=2, pady=(6, 1))

    Eusername = Entry(card, width=28, font=FM(10), bg=PILL_BG, bd=0)
    Eusername.grid(row=4, column=0, columnspan=2, ipady=7, padx=2)
    Frame(card, height=2, bg=ACCENT).grid(row=5, column=0, columnspan=2,
                                           sticky="ew", padx=2, pady=(0, 4))

    # ── Password ──────────────────────────────────────────────────────────────
    password_lbl = Label(card, text=i18n.t("login", "password"), font=FM(9),
                         bg=CARD, anchor="w")
    password_lbl.grid(row=6, column=0, columnspan=2, sticky="w", padx=2, pady=(6, 1))

    Epassword = Entry(card, width=28, font=FM(10), show="*",
                      bg=PILL_BG, relief="flat", bd=0)
    Epassword.grid(row=7, column=0, columnspan=2, ipady=7, padx=2)
    Frame(card, height=2, bg=ACCENT).grid(row=8, column=0, columnspan=2,
                                           sticky="ew", padx=2, pady=(0, 4))

    # ── Show/Hide ─────────────────────────────────────────────────────────────
    toggle_btn = Label(card, text=i18n.t("login", "show"),
                       font=FM(8), bg=PILL_BG, fg=TEXT_LIGHT, cursor="hand2")
    toggle_btn.grid(row=7, column=1, sticky="e", padx=6)

    def toggle_password():
        if Epassword.cget("show") == "":
            Epassword.config(show="*")
            toggle_btn.config(text=i18n.t("login", "show"), fg=TEXT_LIGHT)
        else:
            Epassword.config(show="")
            toggle_btn.config(text=i18n.t("login", "hide"), fg=ACCENT)

    toggle_btn.bind("<Button-1>", lambda e: toggle_password())

    # ── Login button ──────────────────────────────────────────────────────────
    def logindone():
        controller("dashboard")

    def on_enter(e): login_btn.config(bg="#236358")
    def on_leave(e): login_btn.config(bg=ACCENT)

    login_btn = Button(card, text=i18n.t("login", "sign_in"),
                       font=FM(10, "bold"), bg=ACCENT, fg="white", bd=0,
                       activebackground="#236358", activeforeground="white",
                       pady=8, cursor="hand2", command=logindone)
    login_btn.grid(row=9, column=0, columnspan=2, sticky="ew", padx=2, pady=(14, 0))
    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)

    # ── Sign up link ──────────────────────────────────────────────────────────
    bottom = Frame(card, bg=CARD)
    bottom.grid(row=10, column=0, columnspan=2, pady=(10, 0))

    no_account_lbl = Label(bottom, text=i18n.t("login", "no_account"),
                           font=FM(9), bg=CARD, fg=TEXT_MED)
    no_account_lbl.pack(side="left")

    signup_link = Label(bottom, text=i18n.t("login", "sign_up"),
                        font=FM(9, "bold"), bg=CARD, fg=ACCENT, cursor="hand2")
    signup_link.pack(side="left")
    signup_link.bind("<Button-1>", lambda e: controller("signup"))

    # ── Refresh on language change ────────────────────────────────────────────
    def refresh():
        app_lbl.config(text=i18n.t("app_name"))
        subtitle_lbl.config(text=i18n.t("login", "subtitle"))
        username_lbl.config(text=i18n.t("login", "username"))
        password_lbl.config(text=i18n.t("login", "password"))
        login_btn.config(text=i18n.t("login", "sign_in"))
        no_account_lbl.config(text=i18n.t("login", "no_account"))
        signup_link.config(text=i18n.t("login", "sign_up"))
        # keep show/hide in sync with current toggle state
        if Epassword.cget("show") == "*":
            toggle_btn.config(text=i18n.t("login", "show"))
        else:
            toggle_btn.config(text=i18n.t("login", "hide"))

    i18n.on_change(refresh)

    return frame
