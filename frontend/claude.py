import tkinter as tk
from tkinter import font as tkfont
import math, time, threading

# ── Palette ────────────────────────────────────────────────────────────────
BG          = "#F5F0E8"          # warm parchment
CARD        = "#FFFFFF"
ACCENT      = "#2D7D6F"          # teal-green (medical + calm)
ACCENT2     = "#E8834A"          # warm orange for alerts/highlights
TEXT_DARK   = "#1A2B2A"
TEXT_MED    = "#4A6560"
TEXT_LIGHT  = "#8FA8A3"
PILL_BG     = "#E6F4F1"
DANGER      = "#C0392B"
WARN        = "#E67E22"
SAFE        = "#27AE60"

# ── Root ───────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("MediTrack")
root.geometry("1100x720")
root.configure(bg=BG)
root.resizable(True, True)

# ── Fonts ──────────────────────────────────────────────────────────────────
def F(size, weight="normal", slant="roman"):
    return tkfont.Font(family="Georgia", size=size, weight=weight, slant=slant)

def FM(size, weight="normal"):
    return tkfont.Font(family="Helvetica", size=size, weight=weight)

# ── Rounded-rect helper ────────────────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r=16, **kw):
    pts = [
        x1+r, y1,   x2-r, y1,
        x2,   y1,   x2,   y1+r,
        x2,   y2-r, x2,   y2,
        x2-r, y2,   x1+r, y2,
        x1,   y2,   x1,   y2-r,
        x1,   y1+r, x1,   y1,
        x1+r, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kw)

# ══════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
sidebar = tk.Frame(root, bg=ACCENT, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

# Logo area
logo_frame = tk.Frame(sidebar, bg=ACCENT, pady=28)
logo_frame.pack(fill="x")

logo_cv = tk.Canvas(logo_frame, width=48, height=48, bg=ACCENT,
                    highlightthickness=0)
logo_cv.pack()
logo_cv.create_oval(4, 4, 44, 44, fill="white", outline="")
logo_cv.create_text(24, 24, text="✚", font=FM(22, "bold"), fill=ACCENT)

tk.Label(logo_frame, text="MediTrack", font=F(16, "bold"),
         bg=ACCENT, fg="white").pack()
tk.Label(logo_frame, text="Your health companion", font=FM(9),
         bg=ACCENT, fg="#A8D4CE").pack()

tk.Frame(sidebar, bg="#236358", height=1).pack(fill="x", padx=20, pady=4)

# Nav items
nav_items = [
    ("🏠", "Dashboard",      True),
    ("💊", "My Medicines",   False),
    ("⏰", "Reminders",      False),
    ("📋", "Medical History",False),
    ("⚠️", "Interactions",   False),
    ("🍎", "Food & Diet",    False),
    ("👤", "Profile",        False),
]

nav_buttons = []

# def make_nav(icon, label, active):
#     frame = tk.Frame(sidebar, bg=ACCENT if not active else "#236358",
#                      cursor="hand2")
#     frame.pack(fill="x", padx=12, pady=2)

#     # if active:
#     #     accent_bar = tk.Frame(frame, bg=ACCENT2, width=4)
#     #     accent_bar.pack(side="left", fill="y", ipadx=0)

#     inner = tk.Frame(frame, bg=frame["bg"], padx=12, pady=10)
#     inner.pack(side="left", fill="x", expand=True)

#     tk.Label(inner, text=icon, font=FM(14), bg=frame["bg"],
#              fg="white").pack(side="left", padx=(0, 10))
#     tk.Label(inner, text=label, font=FM(11, "bold" if active else "normal"),
#              bg=frame["bg"], fg="white" if active else "#A8D4CE").pack(side="left")

#     def on_enter(e): frame.configure(bg="#236358"); inner.configure(bg="#236358")
#     def on_leave(e):
#         col = "#236358" if active else ACCENT
#         frame.configure(bg=col); inner.configure(bg=col)
#     frame.bind("<Enter>", on_enter); frame.bind("<Leave>", on_leave)
#     inner.bind("<Enter>", on_enter); inner.bind("<Leave>", on_leave)

def make_nav(icon, label, active):
    frame = tk.Frame(sidebar, bg=ACCENT if not active else "#236358",
                     cursor="hand2")
    frame.pack(fill="x", padx=12, pady=2)


    if active:
        accent_bar = tk.Frame(frame, bg=ACCENT2, width=4)
        accent_bar.pack(side="left", fill="y", ipadx=0)

    inner = tk.Frame(frame, bg=frame["bg"], padx=12, pady=10)
    inner.pack(side="left", fill="x", expand=True)

    icon_lbl = tk.Label(inner, text=icon, font=FM(14),
                        bg=frame["bg"], fg="white")
    icon_lbl.pack(side="left", padx=(0, 10))

    text_lbl = tk.Label(inner, text=label,
                        font=FM(11, "bold" if active else "normal"),
                        bg=frame["bg"],
                        fg="white" if active else "#A8D4CE")
    text_lbl.pack(side="left")

    def on_enter(e):
        frame.config(bg="#236358")
        inner.config(bg="#236358")
        icon_lbl.config(bg="#236358")
        text_lbl.config(bg="#236358")

    def on_leave(e):
        col = "#236358" if active else ACCENT
        frame.config(bg=col)
        inner.config(bg=col)
        icon_lbl.config(bg=col)
        text_lbl.config(bg=col)

    for w in [frame, inner, icon_lbl, text_lbl]:
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)

for icon, label, active in nav_items:
    make_nav(icon, label, active)

# Bottom: user card
tk.Frame(sidebar, bg="#236358", height=1).pack(fill="x", padx=20, pady=10,
                                                side="bottom")
user_frame = tk.Frame(sidebar, bg=ACCENT, pady=16)
user_frame.pack(side="bottom", fill="x")

av_cv = tk.Canvas(user_frame, width=42, height=42, bg=ACCENT, 
                  highlightthickness=0)
av_cv.pack()
av_cv.create_oval(2, 2, 40, 40, fill=ACCENT2, outline="")
av_cv.create_text(21, 21, text="M", font=FM(16, "bold"), fill="white")

tk.Label(user_frame, text="Meena Sharma", font=FM(10, "bold"),
         bg=ACCENT, fg="white").pack()
tk.Label(user_frame, text="Patient · 68 yrs", font=FM(9),
         bg=ACCENT, fg="#A8D4CE").pack()

# ══════════════════════════════════════════════════════════════════════════
#  MAIN AREA
# ══════════════════════════════════════════════════════════════════════════
main = tk.Frame(root, bg=BG)
main.pack(side="left", fill="both", expand=True)

# Scrollable canvas
scroll_canvas = tk.Canvas(main, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(main, orient="vertical",
                          command=scroll_canvas.yview)
scroll_canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
scroll_canvas.pack(side="left", fill="both", expand=True)

content = tk.Frame(scroll_canvas, bg=BG)
content_window = scroll_canvas.create_window((0, 0), window=content,
                                              anchor="nw")

def on_configure(e):
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    scroll_canvas.itemconfig(content_window,
                              width=scroll_canvas.winfo_width())
content.bind("<Configure>", on_configure)
scroll_canvas.bind("<Configure>",
    lambda e: scroll_canvas.itemconfig(content_window,
                                        width=e.width))
scroll_canvas.bind_all("<MouseWheel>",
    lambda e: scroll_canvas.yview_scroll(-1*(e.delta//120), "units"))

# ── Top bar ────────────────────────────────────────────────────────────────
topbar = tk.Frame(content, bg=BG, pady=20, padx=30)
topbar.pack(fill="x")

left_top = tk.Frame(topbar, bg=BG)
left_top.pack(side="left")

tk.Label(left_top, text="Good morning, Meena 🌿",
         font=F(20, "bold"), bg=BG, fg=TEXT_DARK).pack(anchor="w")
tk.Label(left_top, text="Here's your health overview for today.",
         font=FM(11), bg=BG, fg=TEXT_MED).pack(anchor="w")

right_top = tk.Frame(topbar, bg=BG)
right_top.pack(side="right")

# Live clock
clock_label = tk.Label(right_top, text="", font=F(13, "bold"),
                        bg=BG, fg=ACCENT)
clock_label.pack(anchor="e")

date_label = tk.Label(right_top, text="", font=FM(10),
                       bg=BG, fg=TEXT_LIGHT)
date_label.pack(anchor="e")

def update_clock():
    while True:
        now = time.localtime()
        clock_label.config(text=time.strftime("%I:%M %p", now))
        date_label.config(text=time.strftime("%A, %d %B %Y", now))
        time.sleep(1)
threading.Thread(target=update_clock, daemon=True).start()

# ── Stat cards ─────────────────────────────────────────────────────────────
stats_frame = tk.Frame(content, bg=BG, padx=30)
stats_frame.pack(fill="x", pady=(0, 6))

stats = [
    ("💊", "Active Medicines", "5", None),
    ("✅", "Taken Today",      "3 / 5", SAFE),
    ("⚠️", "Interactions",    "2 flagged", WARN),
    ("📅", "Days Remaining",  "12 days", ACCENT),
]

for i, (icon, title, val, color) in enumerate(stats):
    card = tk.Frame(stats_frame, bg=CARD, padx=20, pady=18,
                    relief="flat", bd=0)
    card.grid(row=0, column=i, padx=8, pady=4, sticky="nsew")
    stats_frame.columnconfigure(i, weight=1)

    top_row = tk.Frame(card, bg=CARD)
    top_row.pack(anchor="w", fill="x")
    tk.Label(top_row, text=icon, font=FM(18), bg=CARD).pack(side="left")

    tk.Label(card, text=title, font=FM(10), bg=CARD,
             fg=TEXT_LIGHT).pack(anchor="w", pady=(6, 0))
    tk.Label(card, text=val, font=F(20, "bold"), bg=CARD,
             fg=color or TEXT_DARK).pack(anchor="w")

# ══════════════════════════════════════════════════════════════════════════
#  TWO-COLUMN LAYOUT
# ══════════════════════════════════════════════════════════════════════════
cols = tk.Frame(content, bg=BG, padx=22)
cols.pack(fill="both", expand=True, pady=10)
cols.columnconfigure(0, weight=3)
cols.columnconfigure(1, weight=2)

# ── LEFT COLUMN ────────────────────────────────────────────────────────────
left_col = tk.Frame(cols, bg=BG)
left_col.grid(row=0, column=0, sticky="nsew", padx=8)

# Section header helper
def section_header(parent, title, btn_text=None, btn_cmd=None):
    row = tk.Frame(parent, bg=BG)
    row.pack(fill="x", pady=(14, 6))
    tk.Label(row, text=title, font=F(13, "bold"),
             bg=BG, fg=TEXT_DARK).pack(side="left")
    if btn_text:
        b = tk.Label(row, text=btn_text, font=FM(10),
                     bg=PILL_BG, fg=ACCENT, padx=10, pady=4,
                     cursor="hand2")
        b.pack(side="right")
        if btn_cmd: b.bind("<Button-1>", btn_cmd)

# ── Today's Medicines ──────────────────────────────────────────────────────
section_header(left_col, "Today's Medicines", "+ Add Medicine")

medicines = [
    ("Metformin 500mg",   "1 tablet",  "8:00 AM",  True,  "Diabetes"),
    ("Amlodipine 5mg",    "1 tablet",  "8:00 AM",  True,  "BP"),
    ("Vitamin D3",        "1 capsule", "12:00 PM", False, "Supplement"),
    ("Atorvastatin 10mg", "1 tablet",  "9:00 PM",  False, "Cholesterol"),
    ("Aspirin 75mg",      "1 tablet",  "9:00 PM",  False, "Heart"),
]

checked_vars = []

for name, dose, timing, taken, tag in medicines:
    m_card = tk.Frame(left_col, bg=CARD, padx=16, pady=12, relief="flat")
    m_card.pack(fill="x", pady=4)

    var = tk.BooleanVar(value=taken)
    checked_vars.append(var)

    left = tk.Frame(m_card, bg=CARD)
    left.pack(side="left", fill="x", expand=True)

    top = tk.Frame(left, bg=CARD)
    top.pack(anchor="w", fill="x")

    chk = tk.Checkbutton(top, variable=var, bg=CARD,
                          activebackground=CARD,
                          selectcolor=ACCENT, fg=ACCENT,
                          relief="flat", cursor="hand2")
    chk.pack(side="left")

    tk.Label(top, text=name, font=FM(11, "bold"),
             bg=CARD, fg=TEXT_DARK if not taken else TEXT_LIGHT).pack(side="left", padx=4)

    tag_lbl = tk.Label(top, text=tag, font=FM(8),
                        bg=PILL_BG, fg=ACCENT, padx=6, pady=2)
    tag_lbl.pack(side="left", padx=4)

    bot = tk.Frame(left, bg=CARD)
    bot.pack(anchor="w")
    tk.Label(bot, text=f"{dose}  ·  {timing}", font=FM(9),
             bg=CARD, fg=TEXT_LIGHT).pack(side="left")

    status = "✓ Taken" if taken else "⏳ Pending"
    s_col  = SAFE if taken else WARN
    tk.Label(m_card, text=status, font=FM(9, "bold"),
             bg=CARD, fg=s_col).pack(side="right")

# ── Drug Interactions ──────────────────────────────────────────────────────
section_header(left_col, "Drug Interaction Alerts", "View All")

interactions = [
    ("Metformin + Aspirin", "Mild — may increase bleeding risk slightly.", WARN),
    ("Amlodipine + Atorvastatin", "Moderate — monitor muscle pain.", DANGER),
]

for pair, desc, severity in interactions:
    ic = tk.Frame(left_col, bg=CARD, padx=16, pady=12)
    ic.pack(fill="x", pady=4)

    bar = tk.Frame(ic, bg=severity, width=4)
    bar.pack(side="left", fill="y", padx=(0, 12))

    inner = tk.Frame(ic, bg=CARD)
    inner.pack(side="left", fill="x", expand=True)

    tk.Label(inner, text=pair, font=FM(11, "bold"),
             bg=CARD, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(inner, text=desc, font=FM(9), bg=CARD,
             fg=TEXT_MED, wraplength=380, justify="left").pack(anchor="w")

    sev_text = "⚠ Mild" if severity == WARN else "🔴 Moderate"
    tk.Label(ic, text=sev_text, font=FM(9, "bold"),
             bg=CARD, fg=severity).pack(side="right", anchor="n")

# ── RIGHT COLUMN ───────────────────────────────────────────────────────────
right_col = tk.Frame(cols, bg=BG)
right_col.grid(row=0, column=1, sticky="nsew", padx=8)

# ── Next Reminder ──────────────────────────────────────────────────────────
section_header(right_col, "Next Reminder")

rem_card = tk.Frame(right_col, bg=ACCENT, padx=20, pady=18)
rem_card.pack(fill="x", pady=4)

tk.Label(rem_card, text="💊 Vitamin D3", font=F(14, "bold"),
         bg=ACCENT, fg="white").pack(anchor="w")
tk.Label(rem_card, text="1 capsule · 12:00 PM",
         font=FM(11), bg=ACCENT, fg="#A8D4CE").pack(anchor="w")

tk.Frame(rem_card, bg="#236358", height=1).pack(fill="x", pady=10)

bottom_rem = tk.Frame(rem_card, bg=ACCENT)
bottom_rem.pack(fill="x")
tk.Label(bottom_rem, text="🔔 WhatsApp reminder set",
         font=FM(9), bg=ACCENT, fg="#A8D4CE").pack(side="left")
tk.Label(bottom_rem, text="In 1h 23m", font=FM(9, "bold"),
         bg=ACCENT, fg=ACCENT2).pack(side="right")

# ── Adherence Ring ─────────────────────────────────────────────────────────
section_header(right_col, "Weekly Adherence")

ring_frame = tk.Frame(right_col, bg=CARD, pady=20)
ring_frame.pack(fill="x", pady=4)

cv = tk.Canvas(ring_frame, width=160, height=160, bg=CARD,
               highlightthickness=0)
cv.pack()

cx, cy, r_out, r_in = 80, 80, 68, 50
pct = 0.74  # 74% adherence

# Background ring
cv.create_arc(cx-r_out, cy-r_out, cx+r_out, cy+r_out,
              start=90, extent=-360,
              outline="#E8EDE9", width=18, style="arc")
# Filled arc
cv.create_arc(cx-r_out, cy-r_out, cx+r_out, cy+r_out,
              start=90, extent=-(360*pct),
              outline=ACCENT, width=18, style="arc")

cv.create_text(cx, cy-8, text="74%", font=F(20, "bold"), fill=ACCENT)
cv.create_text(cx, cy+12, text="adherence", font=FM(9), fill=TEXT_LIGHT)

days_frame = tk.Frame(ring_frame, bg=CARD)
days_frame.pack()

day_data = [("M", True), ("T", True), ("W", True), ("T", False),
            ("F", True), ("S", True), ("S", False)]
for day, done in day_data:
    d = tk.Frame(days_frame, bg=CARD)
    d.pack(side="left", padx=4)
    dot_cv = tk.Canvas(d, width=28, height=28, bg=CARD, highlightthickness=0)
    dot_cv.pack()
    dot_cv.create_oval(3, 3, 25, 25,
                       fill=SAFE if done else "#EEE", outline="")
    dot_cv.create_text(14, 14, text=day, font=FM(8, "bold"),
                        fill="white" if done else TEXT_LIGHT)

# ── Food & Allergy Alerts ──────────────────────────────────────────────────
section_header(right_col, "Food Alerts")

foods = [
    ("🍊", "Grapefruit", "Avoid — reacts with Amlodipine"),
    ("🧀", "Aged Cheese", "Caution with current BP meds"),
    ("🥗", "Leafy greens", "Safe · Good for Metformin users"),
]

for icon, food, note in foods:
    fc = tk.Frame(right_col, bg=CARD, padx=14, pady=10)
    fc.pack(fill="x", pady=3)

    tk.Label(fc, text=icon, font=FM(16), bg=CARD).pack(side="left", padx=(0,10))
    inner = tk.Frame(fc, bg=CARD)
    inner.pack(side="left")
    tk.Label(inner, text=food, font=FM(10, "bold"), bg=CARD,
             fg=TEXT_DARK).pack(anchor="w")
    col = DANGER if "Avoid" in note else (WARN if "Caution" in note else SAFE)
    tk.Label(inner, text=note, font=FM(9), bg=CARD,
             fg=col).pack(anchor="w")

# ── Quick Action Buttons ───────────────────────────────────────────────────
section_header(right_col, "Quick Actions")

qbtns = tk.Frame(right_col, bg=BG)
qbtns.pack(fill="x", pady=(0, 20))

actions = [
    ("📷 Scan Medicine", ACCENT),
    ("🎤 Voice Input",   ACCENT2),
    ("📞 Call Caregiver", TEXT_MED),
    ("📊 Health Report", TEXT_MED),
]

for i, (label, color) in enumerate(actions):
    btn = tk.Label(qbtns, text=label, font=FM(10, "bold"),
                   bg=color, fg="white",
                   padx=10, pady=10, cursor="hand2")
    btn.grid(row=i//2, column=i%2, padx=4, pady=4, sticky="ew")
    qbtns.columnconfigure(i%2, weight=1)

    def enter(e, b=btn, c=color):
        r, g, b2 = int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)
        darker = f"#{max(0,r-30):02x}{max(0,g-30):02x}{max(0,b2-30):02x}"
        b.configure(bg=darker)
    def leave(e, b=btn, c=color): b.configure(bg=c)
    btn.bind("<Enter>", enter); btn.bind("<Leave>", leave)

# ══════════════════════════════════════════════════════════════════════════
root.mainloop()