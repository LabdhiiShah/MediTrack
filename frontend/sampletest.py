import tkinter as tk
from tkinter import font as tkfont
import math, time

# ── DEBUG ────────────────────────────────────────────────────────────────
DEBUG = True

def dbg_frame(parent, **kwargs):
    if DEBUG:
        return tk.Frame(parent, bd=1, relief="solid", **kwargs)
    else:
        return tk.Frame(parent, **kwargs)

# ── Palette ────────────────────────────────────────────────────────────────
BG          = "#F5F0E8"
CARD        = "#FFFFFF"
ACCENT      = "#2D7D6F"
ACCENT2     = "#E8834A"
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

# ── Fonts ──────────────────────────────────────────────────────────────────
def F(size, weight="normal", slant="roman"):
    return tkfont.Font(family="Georgia", size=size, weight=weight, slant=slant)

def FM(size, weight="normal"):
    return tkfont.Font(family="Helvetica", size=size, weight=weight)

# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
sidebar = dbg_frame(root, bg=ACCENT, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

logo_frame = dbg_frame(sidebar, bg=ACCENT, pady=28)
logo_frame.pack(fill="x")

logo_cv = tk.Canvas(logo_frame, width=48, height=48, bg=ACCENT, highlightthickness=0)
logo_cv.pack()
logo_cv.create_oval(4, 4, 44, 44, fill="white", outline="")
logo_cv.create_text(24, 24, text="✚", font=FM(22, "bold"), fill=ACCENT)

tk.Label(logo_frame, text="MediTrack", font=F(16, "bold"),
         bg=ACCENT, fg="white").pack()

# ══════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ══════════════════════════════════════════════════════════════════════════
main = dbg_frame(root, bg=BG)
main.pack(side="left", fill="both", expand=True)

scroll_canvas = tk.Canvas(main, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(main, orient="vertical", command=scroll_canvas.yview)
scroll_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
scroll_canvas.pack(side="left", fill="both", expand=True)

content = dbg_frame(scroll_canvas, bg=BG)
content_window = scroll_canvas.create_window((0, 0), window=content, anchor="nw")

def on_configure(e):
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

content.bind("<Configure>", on_configure)

# ══════════════════════════════════════════════════════════════════════════
# TOP BAR
# ══════════════════════════════════════════════════════════════════════════
topbar = dbg_frame(content, bg=BG, pady=20, padx=30)
topbar.pack(fill="x")

left_top = dbg_frame(topbar, bg=BG)
left_top.pack(side="left")

tk.Label(left_top, text="Good morning, Meena 🌿",
         font=F(20, "bold"), bg=BG).pack()

right_top = dbg_frame(topbar, bg=BG)
right_top.pack(side="right")

clock_label = tk.Label(right_top, text="", font=F(13, "bold"), bg=BG)
clock_label.pack()

date_label = tk.Label(right_top, text="", font=FM(10), bg=BG)
date_label.pack()

def update_clock():
    now = time.localtime()
    clock_label.config(text=time.strftime("%I:%M %p", now))
    date_label.config(text=time.strftime("%A, %d %B %Y", now))
    root.after(1000, update_clock)

update_clock()

# ══════════════════════════════════════════════════════════════════════════
# STATS
# ══════════════════════════════════════════════════════════════════════════
stats_frame = dbg_frame(content, bg=BG, padx=30)
stats_frame.pack(fill="x")

for i in range(4):
    card = dbg_frame(stats_frame, bg=CARD, padx=20, pady=18)
    card.grid(row=0, column=i, padx=8, sticky="nsew")
    stats_frame.columnconfigure(i, weight=1)

    tk.Label(card, text=f"Card {i+1}", bg=CARD).pack()

# ══════════════════════════════════════════════════════════════════════════
# TWO COLUMN
# ══════════════════════════════════════════════════════════════════════════
cols = dbg_frame(content, bg=BG)
cols.pack(fill="both", expand=True)

cols.columnconfigure(0, weight=3)
cols.columnconfigure(1, weight=2)

left_col = dbg_frame(cols, bg=BG)
left_col.grid(row=0, column=0, sticky="nsew")

right_col = dbg_frame(cols, bg=BG)
right_col.grid(row=0, column=1, sticky="nsew")

# LEFT SAMPLE
for i in range(3):
    c = dbg_frame(left_col, bg=CARD, padx=10, pady=10)
    c.pack(fill="x", pady=5)
    tk.Label(c, text=f"Left Card {i+1}", bg=CARD).pack()

# RIGHT SAMPLE
for i in range(3):
    c = dbg_frame(right_col, bg=CARD, padx=10, pady=10)
    c.pack(fill="x", pady=5)
    tk.Label(c, text=f"Right Card {i+1}", bg=CARD).pack()

# ══════════════════════════════════════════════════════════════════════════
root.mainloop()