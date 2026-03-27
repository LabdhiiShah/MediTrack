from tkinter import *
from frontend.sidebar import create_sidebar
from frontend.addMedicine import add_medicine_popup
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM
from i18n import i18n

SAFE = "#27AE60"

def mymedicinepage(parent, controller):
    frame = Frame(parent, bg=BG)

    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    create_sidebar(container, controller, "My Medicines")

    main = Frame(container, bg=BG)
    main.pack(side="left", fill="both", expand=True)

    # ── Header ────────────────────────────────────────────────────────────────
    title_lbl = Label(main, text=i18n.t("medicines", "title"),
                      bg=BG, font=F(20, "bold"), fg=TEXT_DARK, anchor="w")
    title_lbl.pack(fill="x", padx=20, pady=(20, 4))

    subtitle_lbl = Label(main, text=i18n.t("medicines", "subtitle"),
                         bg=BG, font=F(13), fg=TEXT_MED, anchor="w")
    subtitle_lbl.pack(fill="x", padx=20)

    Frame(main, height=1, bg="#DDD8CC").pack(fill="x", pady=10)

    allmedicines = Frame(main, bg=BG)
    allmedicines.pack(fill="x", padx=32, pady=10)

    # ── Current section ───────────────────────────────────────────────────────
    curr_section_lbl = Label(allmedicines, text=i18n.t("medicines", "current_section"),
                              font=FM(12, "bold"), bg="#F0F7F5", fg=ACCENT,
                              anchor="w", padx=20, pady=10)
    curr_section_lbl.pack(fill="x")

    current_frame = Frame(allmedicines, bg=BG)
    current_frame.pack(fill="x")

    # ── Past section ──────────────────────────────────────────────────────────
    past_section_lbl = Label(allmedicines, text=i18n.t("medicines", "past_section"),
                              font=FM(12, "bold"), bg="#F0F7F5", fg=TEXT_MED,
                              anchor="w", padx=20, pady=10)
    past_section_lbl.pack(fill="x", pady=(10, 0))

    past_frame = Frame(allmedicines, bg=BG)
    past_frame.pack(fill="x")

    medicines = ["Metformin", "Amlodipine", "Vitamin", "Atorvastatin", "Aspirin"]

    # track all medicine status labels for language refresh
    status_labels = []

    def add_card(name, active=True):
        parent_frame = current_frame if active else past_frame

        med = Frame(parent_frame, bg=CARD, padx=20, pady=12,
                    highlightthickness=1,
                    highlightbackground="#D8EAE7" if active else "#E0E0E0")
        med.pack(fill="x", pady=3)

        left = Frame(med, bg=CARD)
        left.pack(side="left", fill="x", expand=True)

        Label(left, text=name, font=FM(11), bg=CARD,
              fg=TEXT_DARK if active else TEXT_LIGHT).pack(anchor="w")

        state = {"active": active}

        status_lbl = Label(med,
                           text=i18n.t("medicines", "status_current" if active else "status_past"),
                           font=FM(9, "bold"), bg=CARD,
                           fg=SAFE if active else TEXT_LIGHT,
                           cursor="hand2")
        status_lbl.pack(side="right", anchor="n")

        # store reference: (label, state dict) so refresh can update text
        status_labels.append((status_lbl, state))

        def toggle():
            state["active"] = not state["active"]
            med.destroy()
            # remove dead label ref
            status_labels[:] = [(l, s) for l, s in status_labels if str(l) != str(status_lbl)]
            add_card(name, active=state["active"])

        status_lbl.bind("<Button-1>", lambda e: toggle())

    for name in medicines:
        add_card(name)

    # ── Add button ────────────────────────────────────────────────────────────
    plus_btn = Label(main, text=i18n.t("medicines", "add_btn"),
                     font=FM(10, "bold"), bg=ACCENT, fg="white",
                     padx=14, pady=8, cursor="hand2")
    plus_btn.pack(anchor="w", padx=32, pady=(12, 0))
    plus_btn.bind("<Button-1>", lambda e: add_medicine_popup(add_card))

    # ── Refresh on language change ────────────────────────────────────────────
    def refresh():
        title_lbl.config(text=i18n.t("medicines", "title"))
        subtitle_lbl.config(text=i18n.t("medicines", "subtitle"))
        curr_section_lbl.config(text=i18n.t("medicines", "current_section"))
        past_section_lbl.config(text=i18n.t("medicines", "past_section"))
        plus_btn.config(text=i18n.t("medicines", "add_btn"))
        for lbl, state in status_labels:
            try:
                key = "status_current" if state["active"] else "status_past"
                lbl.config(text=i18n.t("medicines", key))
            except Exception:
                pass

    i18n.on_change(refresh)

    return frame
