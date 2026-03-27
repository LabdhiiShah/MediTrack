# from tkinter import *
# from frontend.sidebar import create_sidebar
# from scrollable import scrollablefunc
# from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM

# SECTION_BG = "#F0F7F5"
# SAFE       = "#27AE60"
# WARN       = "#E67E22"

# # static medicines list — replace with db query later
# MEDICINES = ["Metformin", "Amlodipine", "Vitamin D3", "Atorvastatin", "Aspirin"]

# def reminderpage(parent, controller):
#     frame = Frame(parent, bg=BG)

#     container = Frame(frame, bg=BG)
#     container.pack(fill="both", expand=True)

#     create_sidebar(container, controller, "Reminders")

#     main = Frame(container, bg=BG)
#     main.pack(side="left", fill="both", expand=True)

#     # header
#     Label(main, text="Reminders", bg=BG, font=F(20, "bold"),
#           fg=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 4))
#     Label(main, text="Never miss a dose", bg=BG, font=F(13),
#           fg=TEXT_MED, anchor="w").pack(fill="x", padx=20)

#     Frame(main, height=1, bg="#DDD8CC").pack(fill="x", pady=10)

#     # section title
#     Label(main, text="Today's Schedule", font=FM(12, "bold"),
#           bg=SECTION_BG, fg=ACCENT, anchor="w",
#           padx=20, pady=10).pack(fill="x", pady=(14, 0))

#     # schedule container
#     schedule = Frame(main, bg=BG)
#     schedule.pack(fill="x", padx=32, pady=10)

#     # static schedule data — replace with db later
#     todays = [
#         ("8:00 AM",  "Metformin",    "1 tablet",   "2 capsules", True),
#         ("12:00 PM", "Vitamin D3",   "1 capsule",  "1 capsule",  False),
#         ("9:00 PM",  "Amlodipine",   "1 tablet",   "1 capsule",  False),
#         ("9:00 PM",  "Atorvastatin", "1 tablet",   "1 capsule",  False),
#     ]

#     for timing, med, dose, capsules, done in todays:
#         card = Frame(schedule, bg=CARD, padx=20, pady=12,
#                      highlightthickness=1, highlightbackground="#D8EAE7")
#         card.pack(fill="x", pady=3)

#         left = Frame(card, bg=CARD)
#         left.pack(side="left", fill="x", expand=True)

#         top = Frame(left, bg=CARD)
#         top.pack(anchor="w")

#         # status dot
#         dot = Canvas(top, width=10, height=10, bg=CARD, highlightthickness=0)
#         dot.pack(side="left", padx=(0, 8))
#         dot.create_oval(1, 1, 9, 9, fill=SAFE if done else WARN, outline="")

#         Label(top, text=med, font=FM(11, "bold"),
#               bg=CARD, fg=TEXT_DARK).pack(side="left")

#         Label(left, text=f"{timing}  ·  {dose}  ·  {capsules}",
#               font=FM(9), bg=CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=(2, 0))

#         Label(card, text="✓ Done" if done else "⏳ Pending",
#               font=FM(9, "bold"), bg=CARD,
#               fg=SAFE if done else WARN).pack(side="right", anchor="n")

#     # + Add Reminder button
#     def add_reminder_popup():
#         popup = Toplevel()
#         popup.title("Add Reminder")
#         popup.geometry("340x280")
#         popup.resizable(False, False)
#         popup.configure(bg=CARD)

#         popup.update_idletasks()
#         x = (popup.winfo_screenwidth()  - 340) // 2
#         y = (popup.winfo_screenheight() - 280) // 2
#         popup.geometry(f"340x280+{x}+{y}")

#         Label(popup, text="Add Reminder", font=F(13, "bold"),
#               bg=CARD, fg=TEXT_DARK).pack(anchor="w", padx=24, pady=(18, 12))

#         def row(label_text):
#             r = Frame(popup, bg=CARD)
#             r.pack(fill="x", padx=24, pady=4)
#             Label(r, text=label_text, font=FM(9), bg=CARD,
#                   fg=TEXT_MED, width=14, anchor="w").pack(side="left")
#             return r

#         # medicine dropdown
#         r1 = row("Medicine")
#         med_var = StringVar(value=MEDICINES[0])
#         OptionMenu(r1, med_var, *MEDICINES).pack(side="left", fill="x", expand=True)

#         # dosage
#         r2 = row("Dosage")
#         dose_var = StringVar(value="1 tablet")
#         Entry(r2, textvariable=dose_var, font=FM(10), width=18,
#               bg="#F5F5F5", relief="flat", bd=0,
#               highlightthickness=1, highlightbackground="#DDD",
#               highlightcolor=ACCENT).pack(side="left", ipady=6)

#         # no. of capsules
#         r3 = row("No. of capsules")
#         cap_var = StringVar(value="1")
#         Entry(r3, textvariable=cap_var, font=FM(10), width=18,
#               bg="#F5F5F5", relief="flat", bd=0,
#               highlightthickness=1, highlightbackground="#DDD",
#               highlightcolor=ACCENT).pack(side="left", ipady=6)

#         # timing
#         r4 = row("Timing")
#         time_var = StringVar(value="8:00 AM")
#         Entry(r4, textvariable=time_var, font=FM(10), width=18,
#               bg="#F5F5F5", relief="flat", bd=0,
#               highlightthickness=1, highlightbackground="#DDD",
#               highlightcolor=ACCENT).pack(side="left", ipady=6)

#         def confirm():
#             med   = med_var.get().strip()
#             dose  = dose_var.get().strip()
#             caps  = cap_var.get().strip()
#             timing = time_var.get().strip()
#             if med and dose and caps and timing:
#                 card = Frame(schedule, bg=CARD, padx=20, pady=12,
#                              highlightthickness=1, highlightbackground="#D8EAE7")
#                 card.pack(fill="x", pady=3)
#                 left = Frame(card, bg=CARD)
#                 left.pack(side="left", fill="x", expand=True)
#                 top = Frame(left, bg=CARD); top.pack(anchor="w")
#                 dot = Canvas(top, width=10, height=10, bg=CARD, highlightthickness=0)
#                 dot.pack(side="left", padx=(0, 8))
#                 dot.create_oval(1, 1, 9, 9, fill=WARN, outline="")
#                 Label(top, text=med, font=FM(11, "bold"),
#                       bg=CARD, fg=TEXT_DARK).pack(side="left")
#                 Label(left, text=f"{timing}  ·  {dose}  ·  {caps} capsules",
#                       font=FM(9), bg=CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=(2, 0))
#                 Label(card, text="⏳ Pending", font=FM(9, "bold"),
#                       bg=CARD, fg=WARN).pack(side="right", anchor="n")
#                 popup.destroy()

#         add_btn = Label(popup, text="Add Reminder", font=FM(10, "bold"),
#                         bg=ACCENT, fg="white", padx=14, pady=8, cursor="hand2")
#         add_btn.pack(anchor="e", padx=24, pady=(14, 0))
#         add_btn.bind("<Button-1>", lambda e: confirm())
#         popup.bind("<Return>", lambda e: confirm())

#     plus_btn = Label(main, text="＋ Add Reminder", font=FM(10, "bold"),
#                      bg=ACCENT, fg="white", padx=14, pady=8, cursor="hand2")
#     plus_btn.pack(anchor="w", padx=32, pady=(8, 0))
#     plus_btn.bind("<Button-1>", lambda e: add_reminder_popup())

#     return frame

from tkinter import *
from tkinter import font as tkfont
from tkcalendar import DateEntry
from frontend.sidebar import create_sidebar
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM

SECTION_BG = "#F0F7F5"
SAFE       = "#27AE60"
WARN       = "#E67E22"
MEDICINES  = ["Metformin", "Amlodipine", "Vitamin D3", "Atorvastatin", "Aspirin"]
DAYS       = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def reminderpage(parent, controller):
    frame = Frame(parent, bg=BG)

    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    create_sidebar(container, controller, "Reminders")

    main = Frame(container, bg=BG)
    main.pack(side="left", fill="both", expand=True)

    # ── Header ───────────────────────────────────────────────────────────────
    Label(main, text="Reminders", bg=BG, font=F(20, "bold"),
          fg=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 4))
    Label(main, text="Never miss a dose", bg=BG, font=F(13),
          fg=TEXT_MED, anchor="w").pack(fill="x", padx=20)
    Frame(main, height=1, bg="#DDD8CC").pack(fill="x", pady=10)

    # ── Section title ─────────────────────────────────────────────────────────
    Label(main, text="Today's Schedule", font=FM(12, "bold"),
          bg=SECTION_BG, fg=ACCENT, anchor="w",
          padx=20, pady=10).pack(fill="x", pady=(14, 0))

    schedule = Frame(main, bg=BG)
    schedule.pack(fill="x", padx=32, pady=10)

    # ── Static data ───────────────────────────────────────────────────────────
    todays = [
        ("8:00 AM",  "Metformin",    2, ["Mon","Tue","Wed","Thu","Fri"], True),
        ("12:00 PM", "Vitamin D3",   1, ["Mon","Wed","Fri"],             False),
        ("9:00 PM",  "Amlodipine",   1, ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], False),
    ]

    def add_schedule_card(timing, med, tablets, days, done=False):
        card = Frame(schedule, bg=CARD, padx=20, pady=12,
                     highlightthickness=1, highlightbackground="#D8EAE7")
        card.pack(fill="x", pady=3)

        left = Frame(card, bg=CARD)
        left.pack(side="left", fill="x", expand=True)

        top = Frame(left, bg=CARD)
        top.pack(anchor="w")

        dot = Canvas(top, width=10, height=10, bg=CARD, highlightthickness=0)
        dot.pack(side="left", padx=(0, 8))
        dot.create_oval(1, 1, 9, 9, fill=SAFE if done else WARN, outline="")

        Label(top, text=med, font=FM(11, "bold"),
              bg=CARD, fg=TEXT_DARK).pack(side="left")

        days_str = "  ·  " + ", ".join(days) if days else ""
        Label(left,
              text=f"{timing}  ·  {tablets} tablet(s){days_str}",
              font=FM(9), bg=CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=(2, 0))

        Label(card, text="✓ Done" if done else "⏳ Pending",
              font=FM(9, "bold"), bg=CARD,
              fg=SAFE if done else WARN).pack(side="right", anchor="n")

    for timing, med, tablets, days, done in todays:
        add_schedule_card(timing, med, tablets, days, done)

    # ── Popup ─────────────────────────────────────────────────────────────────
    def add_reminder_popup():
        popup = Toplevel()
        popup.title("Add Reminder")
        popup.geometry("380x520")
        popup.resizable(False, False)
        popup.configure(bg=CARD)

        popup.update_idletasks()
        x = (popup.winfo_screenwidth()  - 380) // 2
        y = (popup.winfo_screenheight() - 520) // 2
        popup.geometry(f"380x520+{x}+{y}")

        Label(popup, text="Add Reminder", font=F(13, "bold"),
              bg=CARD, fg=TEXT_DARK).pack(anchor="w", padx=24, pady=(18, 4))
        Frame(popup, height=1, bg="#DDD8CC").pack(fill="x", padx=24, pady=(0, 12))

        def section(text):
            Label(popup, text=text, font=FM(9), bg=CARD,
                  fg=TEXT_MED).pack(anchor="w", padx=24, pady=(10, 2))

        # ── Medicine dropdown ─────────────────────────────────────────────────
        section("Medicine")
        med_var = StringVar(value=MEDICINES[0])
        med_row = Frame(popup, bg=CARD)
        med_row.pack(fill="x", padx=24)
        om = OptionMenu(med_row, med_var, *MEDICINES)
        om.config(font=FM(10), bg="#F5F5F5", relief="flat",
                  highlightthickness=1, highlightbackground="#DDD",
                  activebackground=PILL_BG, cursor="hand2", width=28)
        om.pack(fill="x")

        # ── Clock picker ──────────────────────────────────────────────────────
        section("Time")
        clock_frame = Frame(popup, bg=CARD)
        clock_frame.pack(anchor="w", padx=24)

        hour_var = IntVar(value=8)
        min_var  = IntVar(value=0)
        ampm_var = StringVar(value="AM")

        def spin_box(parent, var, from_, to_, width=3):
            f = Frame(parent, bg="#F5F5F5",
                      highlightthickness=1, highlightbackground="#DDD")
            f.pack(side="left", padx=2)
            up   = Label(f, text="▲", font=FM(7), bg="#F5F5F5",
                         fg=ACCENT, cursor="hand2")
            val  = Label(f, text=f"{var.get():02d}", font=FM(13, "bold"),
                         bg="#F5F5F5", fg=TEXT_DARK, width=width)
            down = Label(f, text="▼", font=FM(7), bg="#F5F5F5",
                         fg=ACCENT, cursor="hand2")
            up.pack(pady=(4, 0))
            val.pack()
            down.pack(pady=(0, 4))

            def inc(e):
                v = (var.get() - from_ + 1) % (to_ - from_ + 1) + from_
                var.set(v)
                val.config(text=f"{v:02d}")
            def dec(e):
                v = (var.get() - from_ - 1) % (to_ - from_ + 1) + from_
                var.set(v)
                val.config(text=f"{v:02d}")
            up.bind("<Button-1>", inc)
            down.bind("<Button-1>", dec)
            return f

        spin_box(clock_frame, hour_var, 1, 12)
        Label(clock_frame, text=":", font=FM(14, "bold"),
              bg=CARD, fg=TEXT_DARK).pack(side="left", padx=2)
        spin_box(clock_frame, min_var, 0, 59)

        # AM/PM toggle
        ampm_frame = Frame(clock_frame, bg="#F5F5F5",
                           highlightthickness=1, highlightbackground="#DDD")
        ampm_frame.pack(side="left", padx=8)

        def make_ampm(text):
            lbl = Label(ampm_frame, text=text, font=FM(10, "bold"),
                        bg=ACCENT if ampm_var.get() == text else "#F5F5F5",
                        fg="white" if ampm_var.get() == text else TEXT_MED,
                        padx=10, pady=6, cursor="hand2")
            lbl.pack(side="left")
            def click(e, t=text, l=lbl):
                ampm_var.set(t)
                for w in ampm_frame.winfo_children():
                    w.config(bg=ACCENT if w.cget("text") == t else "#F5F5F5",
                             fg="white" if w.cget("text") == t else TEXT_MED)
            lbl.bind("<Button-1>", click)

        make_ampm("AM")
        make_ampm("PM")

        # ── Tablet count ──────────────────────────────────────────────────────
        section("No. of Tablets")
        tab_frame = Frame(popup, bg=CARD)
        tab_frame.pack(anchor="w", padx=24)

        tab_var = IntVar(value=1)

        dec_btn = Label(tab_frame, text="−", font=FM(14, "bold"),
                        bg="#F5F5F5", fg=ACCENT, padx=12, pady=4,
                        cursor="hand2",
                        highlightthickness=1, highlightbackground="#DDD")
        dec_btn.pack(side="left")

        tab_lbl = Label(tab_frame, text="1", font=FM(13, "bold"),
                        bg=CARD, fg=TEXT_DARK, width=3)
        tab_lbl.pack(side="left", padx=8)

        inc_btn = Label(tab_frame, text="＋", font=FM(14, "bold"),
                        bg="#F5F5F5", fg=ACCENT, padx=12, pady=4,
                        cursor="hand2",
                        highlightthickness=1, highlightbackground="#DDD")
        inc_btn.pack(side="left")

        def inc_tab(e):
            tab_var.set(tab_var.get() + 1)
            tab_lbl.config(text=str(tab_var.get()))
        def dec_tab(e):
            if tab_var.get() > 1:
                tab_var.set(tab_var.get() - 1)
                tab_lbl.config(text=str(tab_var.get()))

        inc_btn.bind("<Button-1>", inc_tab)
        dec_btn.bind("<Button-1>", dec_tab)

        # ── Day selector ──────────────────────────────────────────────────────
        section("Repeat on")
        days_frame = Frame(popup, bg=CARD)
        days_frame.pack(anchor="w", padx=24)

        day_vars = {}
        for day in DAYS:
            v = BooleanVar(value=True)
            day_vars[day] = v
            btn = Label(days_frame, text=day, font=FM(8, "bold"),
                        bg=ACCENT, fg="white", padx=6, pady=5,
                        cursor="hand2", width=3)
            btn.pack(side="left", padx=2)

            def toggle_day(e, b=btn, var=v):
                var.set(not var.get())
                b.config(bg=ACCENT if var.get() else "#E0E0E0",
                         fg="white" if var.get() else TEXT_LIGHT)
            btn.bind("<Button-1>", toggle_day)

        # ── Date range ────────────────────────────────────────────────────────
        date_row = Frame(popup, bg=CARD)
        date_row.pack(fill="x", padx=24, pady=(10, 0))

        Label(date_row, text="Start", font=FM(9), bg=CARD,
              fg=TEXT_MED, width=6, anchor="w").pack(side="left")
        start_date = DateEntry(date_row, width=10, font=FM(10),
                               background=ACCENT, foreground="white",
                               bordercolor=ACCENT, headersbackground=ACCENT,
                               normalbackground=PILL_BG, normalforeground=TEXT_DARK,
                               selectbackground=ACCENT, selectforeground="white",
                               relief="flat")
        start_date.pack(side="left", padx=(0, 16))

        Label(date_row, text="End", font=FM(9), bg=CARD,
              fg=TEXT_MED, width=4, anchor="w").pack(side="left")
        end_date = DateEntry(date_row, width=10, font=FM(10),
                             background=ACCENT, foreground="white",
                             bordercolor=ACCENT, headersbackground=ACCENT,
                             normalbackground=PILL_BG, normalforeground=TEXT_DARK,
                             selectbackground=ACCENT, selectforeground="white",
                             relief="flat")
        end_date.pack(side="left")

        # ── Confirm ───────────────────────────────────────────────────────────
        def confirm():
            med     = med_var.get()
            h       = hour_var.get()
            m       = min_var.get()
            ap      = ampm_var.get()
            tabs    = tab_var.get()
            sel_days = [d for d, v in day_vars.items() if v.get()]
            timing  = f"{h:02d}:{m:02d} {ap}"
            if med and sel_days:
                add_schedule_card(timing, med, tabs, sel_days, done=False)
                popup.destroy()

        Frame(popup, height=1, bg="#DDD8CC").pack(fill="x", padx=24, pady=(14, 0))
        add_btn = Label(popup, text="Add Reminder", font=FM(10, "bold"),
                        bg=ACCENT, fg="white", padx=14, pady=9, cursor="hand2")
        add_btn.pack(anchor="e", padx=24, pady=(10, 0))
        add_btn.bind("<Button-1>", lambda e: confirm())

    # ── + button ──────────────────────────────────────────────────────────────
    plus_btn = Label(main, text="＋ Add Reminder", font=FM(10, "bold"),
                     bg=ACCENT, fg="white", padx=14, pady=8, cursor="hand2")
    plus_btn.pack(anchor="w", padx=32, pady=(8, 0))
    plus_btn.bind("<Button-1>", lambda e: add_reminder_popup())

    return frame