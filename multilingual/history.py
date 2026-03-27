from tkinter import *
from frontend.sidebar import create_sidebar
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM
from i18n import i18n

def historypage(parent, controller):
    frame = Frame(parent, bg=BG)

    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    create_sidebar(container, controller, "Medical History")

    right = Frame(container, bg=BG)
    right.pack(side="left", fill="both", expand=True)

    con = scrollablefunc(right, BG)

    # ── Header ────────────────────────────────────────────────────────────────
    main = Frame(con, bg=BG)
    main.pack(fill="x", padx=20, pady=(20, 4))

    title_lbl = Label(main, text=i18n.t("history", "title"),
                      bg=BG, font=F(20, "bold"), fg=TEXT_DARK, anchor="w")
    title_lbl.pack(side="left")

    edit_lbl = Label(main, text=i18n.t("history", "edit"),
                     font=FM(10, "bold"), bg=ACCENT, fg="white",
                     padx=12, pady=6, cursor="hand2")
    edit_lbl.pack(side="right")

    subtitle_lbl = Label(con, text=i18n.t("history", "subtitle"),
                         bg=BG, font=F(13), fg=TEXT_MED, anchor="w")
    subtitle_lbl.pack(fill="x", padx=20)

    Frame(con, height=1, bg=ACCENT).pack(fill="x", pady=10)

    # ── Refresh on language change ────────────────────────────────────────────
    def refresh():
        try:
            title_lbl.config(text=i18n.t("history", "title"))
            edit_lbl.config(text=i18n.t("history", "edit"))
            subtitle_lbl.config(text=i18n.t("history", "subtitle"))
        except Exception:
            pass

    i18n.on_change(refresh)

    return frame
