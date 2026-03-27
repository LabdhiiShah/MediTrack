import tkinter as tk
from tkinter import font as tkfont, ttk

# ── Palette (same as your main app) ─────────────────────────────────────────
BG         = "#F5F0E8"
CARD       = "#FFFFFF"
ACCENT     = "#2D7D6F"
ACCENT2    = "#E8834A"
TEXT_DARK  = "#1A2B2A"
TEXT_MED   = "#4A6560"
TEXT_LIGHT = "#8FA8A3"
PILL_BG    = "#E6F4F1"
DANGER     = "#C0392B"
WARN       = "#E67E22"
SAFE       = "#27AE60"
SECTION_BG = "#F0F7F5"   # very light teal tint for section headers

def F(size, weight="normal"):
    return tkfont.Font(family="Georgia", size=size, weight=weight)

def FM(size, weight="normal"):
    return tkfont.Font(family="Helvetica", size=size, weight=weight)

# ════════════════════════════════════════════════════════════════════════════
#  build_medical_history_page(parent)
#  Call this with your content frame / page container.
#  Returns the outermost frame so you can pack/forget it.
# ════════════════════════════════════════════════════════════════════════════
def build_medical_history_page(parent):

    # ── Outer page frame ────────────────────────────────────────────────────
    page = tk.Frame(parent, bg=BG)

    # ── Scrollable canvas setup ─────────────────────────────────────────────
    canvas = tk.Canvas(page, bg=BG, highlightthickness=0)
    vscroll = tk.Scrollbar(page, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vscroll.set)
    vscroll.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner = tk.Frame(canvas, bg=BG)
    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    def _on_inner_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_canvas_configure(e):
        canvas.itemconfig(win_id, width=e.width)

    inner.bind("<Configure>", _on_inner_configure)
    canvas.bind("<Configure>", _on_canvas_configure)
    canvas.bind_all("<MouseWheel>",
        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    # ════════════════════════════════════════════════════════════════════════
    #  HEADER
    # ════════════════════════════════════════════════════════════════════════
    header = tk.Frame(inner, bg=BG, padx=32, pady=24)
    header.pack(fill="x")

    left_h = tk.Frame(header, bg=BG)
    left_h.pack(side="left")

    tk.Label(left_h, text="Medical History",
             font=F(22, "bold"), bg=BG, fg=TEXT_DARK).pack(anchor="w")
    tk.Label(left_h, text="Keep your health records accurate for better care.",
             font=FM(11), bg=BG, fg=TEXT_MED).pack(anchor="w")

    right_h = tk.Frame(header, bg=BG)
    right_h.pack(side="right", anchor="n")

    # Edit / Save toggle button
    edit_state = {"editing": False}

    def toggle_edit():
        if not edit_state["editing"]:
            edit_state["editing"] = True
            edit_btn.configure(text="💾  Save Changes", bg=SAFE)
            _enable_all_entries(True)
        else:
            edit_state["editing"] = False
            edit_btn.configure(text="✏️  Edit History", bg=ACCENT)
            _enable_all_entries(False)
            # TODO: persist data here

    edit_btn = tk.Label(right_h, text="✏️  Edit History",
                        font=FM(10, "bold"), bg=ACCENT, fg="white",
                        padx=16, pady=8, cursor="hand2")
    edit_btn.pack()
    edit_btn.bind("<Button-1>", lambda e: toggle_edit())

    # ── Separator ───────────────────────────────────────────────────────────
    tk.Frame(inner, bg="#DDD8CC", height=1).pack(fill="x", padx=32)

    # ════════════════════════════════════════════════════════════════════════
    #  HELPERS
    # ════════════════════════════════════════════════════════════════════════
    all_entries = []   # collect every Entry/Text so we can enable/disable

    def _enable_all_entries(enabled):
        state = "normal" if enabled else "disabled"
        for w in all_entries:
            try:
                w.configure(state=state)
            except Exception:
                pass

    def section(parent_frame, title, icon):
        """Draws a teal-tinted section header row."""
        sec = tk.Frame(parent_frame, bg=SECTION_BG, padx=20, pady=10)
        sec.pack(fill="x", pady=(18, 0))
        tk.Label(sec, text=f"{icon}  {title}",
                 font=FM(12, "bold"), bg=SECTION_BG, fg=ACCENT).pack(anchor="w")

    def card(parent_frame):
        """White card container."""
        c = tk.Frame(parent_frame, bg=CARD, padx=24, pady=16)
        c.pack(fill="x", padx=32, pady=2)
        return c

    def field_row(parent_frame, label_text, var_or_text=None,
                  width=28, is_text=False, height=3):
        """One label + entry (or Text widget) row inside a card."""
        row = tk.Frame(parent_frame, bg=CARD)
        row.pack(fill="x", pady=5)

        tk.Label(row, text=label_text, font=FM(10),
                 bg=CARD, fg=TEXT_LIGHT, width=20, anchor="w").pack(side="left")

        if is_text:
            txt = tk.Text(row, font=FM(10), fg=TEXT_DARK,
                          bg="#F9F9F9", relief="flat", bd=1,
                          height=height, width=width, wrap="word",
                          state="disabled",
                          highlightthickness=1,
                          highlightbackground="#E0E0E0",
                          highlightcolor=ACCENT)
            txt.insert("1.0", var_or_text or "")
            txt.pack(side="left", fill="x", expand=True)
            all_entries.append(txt)
            return txt
        else:
            var = var_or_text if isinstance(var_or_text, tk.StringVar) \
                  else tk.StringVar(value=var_or_text or "")
            ent = tk.Entry(row, textvariable=var, font=FM(10),
                           fg=TEXT_DARK, bg="#F9F9F9", relief="flat", bd=1,
                           width=width, state="disabled",
                           highlightthickness=1,
                           highlightbackground="#E0E0E0",
                           highlightcolor=ACCENT)
            ent.pack(side="left", fill="x", expand=True)
            all_entries.append(ent)
            return var

    def divider(parent_frame):
        tk.Frame(parent_frame, bg="#F0F0F0", height=1).pack(
            fill="x", padx=32, pady=0)

    # ── Pill / tag list widget ───────────────────────────────────────────────
    def pill_list(parent_frame, items, color=ACCENT, bg=PILL_BG):
        """Displays a horizontal wrapping row of pill tags."""
        wrap = tk.Frame(parent_frame, bg=CARD)
        wrap.pack(anchor="w", fill="x", pady=4)

        def render_pills(pill_items):
            for w in wrap.winfo_children():
                w.destroy()
            row_f = tk.Frame(wrap, bg=CARD)
            row_f.pack(anchor="w")
            for item in pill_items:
                pill = tk.Frame(row_f, bg=bg, padx=10, pady=4)
                pill.pack(side="left", padx=(0, 6), pady=2)
                tk.Label(pill, text=item, font=FM(9), bg=bg, fg=color).pack(side="left")
                x_btn = tk.Label(pill, text=" ✕", font=FM(8),
                                  bg=bg, fg=TEXT_LIGHT, cursor="hand2")
                x_btn.pack(side="left")
                x_btn.bind("<Button-1>",
                           lambda e, it=item: (pill_items.remove(it),
                                               render_pills(pill_items)))
            # "+ Add" button
            add = tk.Label(row_f, text="＋ Add",
                           font=FM(9), bg=CARD, fg=ACCENT,
                           cursor="hand2", padx=6)
            add.pack(side="left", padx=4)
            add.bind("<Button-1>", lambda e: _add_pill_dialog(pill_items, render_pills))

        render_pills(items)
        return items

    def _add_pill_dialog(items, render_fn):
        """Tiny inline entry that appears after ＋ Add."""
        popup = tk.Toplevel()
        popup.title("Add item")
        popup.geometry("280x90")
        popup.configure(bg=CARD)
        popup.resizable(False, False)
        tk.Label(popup, text="Enter value:", font=FM(10),
                 bg=CARD, fg=TEXT_DARK).pack(pady=(12, 4))
        var = tk.StringVar()
        ent = tk.Entry(popup, textvariable=var, font=FM(11),
                       bg="#F9F9F9", relief="flat", bd=1,
                       highlightthickness=1, highlightbackground=ACCENT)
        ent.pack(padx=20, fill="x")
        ent.focus()

        def confirm(e=None):
            val = var.get().strip()
            if val:
                items.append(val)
                render_fn(items)
            popup.destroy()

        ent.bind("<Return>", confirm)
        tk.Label(popup, text="Press Enter to add",
                 font=FM(8), bg=CARD, fg=TEXT_LIGHT).pack(pady=4)

    # ════════════════════════════════════════════════════════════════════════
    #  SECTION 1 — PERSONAL DETAILS
    # ════════════════════════════════════════════════════════════════════════
    section(inner, "Personal Details", "👤")
    c1 = card(inner)

    field_row(c1, "Full Name",    "Meena Sharma")
    divider(c1)
    field_row(c1, "Date of Birth", "12 / 03 / 1957")
    divider(c1)
    field_row(c1, "Age",           "68 years")
    divider(c1)
    field_row(c1, "Gender",        "Female")
    divider(c1)
    field_row(c1, "Blood Group",   "O  Positive")
    divider(c1)
    field_row(c1, "Height",        "158 cm")
    divider(c1)
    field_row(c1, "Weight",        "62 kg")
    divider(c1)
    field_row(c1, "BMI",           "24.8  (Normal)")

    # ════════════════════════════════════════════════════════════════════════
    #  SECTION 2 — EXISTING CONDITIONS
    # ════════════════════════════════════════════════════════════════════════
    section(inner, "Existing Conditions", "🏥")
    c2 = card(inner)

    conditions = ["Type 2 Diabetes", "Hypertension", "Mild Osteoporosis"]

    tk.Label(c2, text="Diagnosed conditions", font=FM(10),
             bg=CARD, fg=TEXT_LIGHT).pack(anchor="w")
    pill_list(c2, conditions, color=ACCENT, bg=PILL_BG)

    divider(c2)

    tk.Label(c2, text="Additional notes", font=FM(10),
             bg=CARD, fg=TEXT_LIGHT, pady=6).pack(anchor="w")
    field_row(c2, "", "Diabetes diagnosed in 2010. BP managed since 2015.",
              is_text=True, height=3)

    # ════════════════════════════════════════════════════════════════════════
    #  SECTION 3 — ALLERGIES
    # ════════════════════════════════════════════════════════════════════════
    section(inner, "Allergies", "⚠️")
    c3 = card(inner)

    med_allergies  = ["Penicillin", "Sulfa drugs"]
    food_allergies = ["Peanuts"]

    r1 = tk.Frame(c3, bg=CARD)
    r1.pack(fill="x", pady=4)
    tk.Label(r1, text="Medicine allergies", font=FM(10),
             bg=CARD, fg=TEXT_LIGHT, width=20, anchor="w").pack(side="left")
    sub1 = tk.Frame(r1, bg=CARD)
    sub1.pack(side="left", fill="x", expand=True)
    pill_list(sub1, med_allergies,
              color="#C0392B", bg="#FDECEA")

    divider(c3)

    r2 = tk.Frame(c3, bg=CARD)
    r2.pack(fill="x", pady=4)
    tk.Label(r2, text="Food allergies", font=FM(10),
             bg=CARD, fg=TEXT_LIGHT, width=20, anchor="w").pack(side="left")
    sub2 = tk.Frame(r2, bg=CARD)
    sub2.pack(side="left", fill="x", expand=True)
    pill_list(sub2, food_allergies,
              color="#E67E22", bg="#FEF3E2")

    divider(c3)

    tk.Label(c3, text="Other / environmental", font=FM(10),
             bg=CARD, fg=TEXT_LIGHT, pady=6).pack(anchor="w")
    field_row(c3, "", "Mild dust allergy — seasonal.", is_text=True, height=2)

    # ════════════════════════════════════════════════════════════════════════
    #  SECTION 4 — PAST SURGERIES & HOSPITALIZATIONS
    # ════════════════════════════════════════════════════════════════════════
    section(inner, "Past Surgeries & Hospitalizations", "🔬")
    c4 = card(inner)

    surgeries = [
        ("Appendectomy",         "2003", "KIMS Hospital, Hyderabad", "Successful"),
        ("Cataract surgery (L)", "2019", "Sankara Eye Hospital",     "Successful"),
    ]

    for i, (proc, year, hospital, outcome) in enumerate(surgeries):
        if i > 0:
            divider(c4)
        row = tk.Frame(c4, bg=CARD, pady=6)
        row.pack(fill="x")

        left_s = tk.Frame(row, bg=CARD)
        left_s.pack(side="left", fill="x", expand=True)

        tk.Label(left_s, text=proc, font=FM(11, "bold"),
                 bg=CARD, fg=TEXT_DARK).pack(anchor="w")
        tk.Label(left_s, text=f"{hospital}  ·  {year}",
                 font=FM(9), bg=CARD, fg=TEXT_LIGHT).pack(anchor="w")

        tk.Label(row, text=f"✓ {outcome}", font=FM(9, "bold"),
                 bg=CARD, fg=SAFE).pack(side="right", anchor="n")

    divider(c4)
    tk.Label(c4, text="Add a record", font=FM(10),
             bg=CARD, fg=ACCENT, cursor="hand2", pady=8).pack(anchor="w")

    # ════════════════════════════════════════════════════════════════════════
    #  SECTION 5 — FAMILY HISTORY
    # ════════════════════════════════════════════════════════════════════════
    section(inner, "Family History", "👨‍👩‍👧")
    c5 = card(inner)

    family = [
        ("Father", "Type 2 Diabetes, Hypertension"),
        ("Mother", "Osteoporosis, Thyroid disorder"),
        ("Sibling","No known conditions"),
    ]

    for i, (relation, history) in enumerate(family):
        if i > 0:
            divider(c5)
        row = tk.Frame(c5, bg=CARD, pady=5)
        row.pack(fill="x")
        tk.Label(row, text=relation, font=FM(10),
                 bg=CARD, fg=TEXT_LIGHT, width=12, anchor="w").pack(side="left")
        field_row(row, "", history, width=40)

    # ════════════════════════════════════════════════════════════════════════
    #  SECTION 6 — LIFESTYLE
    # ════════════════════════════════════════════════════════════════════════
    section(inner, "Lifestyle", "🌿")
    c6 = card(inner)

    def radio_row(parent, label_text, options, default):
        row = tk.Frame(parent, bg=CARD, pady=5)
        row.pack(fill="x")
        tk.Label(row, text=label_text, font=FM(10),
                 bg=CARD, fg=TEXT_LIGHT, width=20, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        for opt in options:
            rb = tk.Radiobutton(row, text=opt, variable=var, value=opt,
                                font=FM(10), bg=CARD, fg=TEXT_DARK,
                                selectcolor=ACCENT, activebackground=CARD,
                                cursor="hand2")
            rb.pack(side="left", padx=8)
        return var

    radio_row(c6, "Smoking",   ["Never", "Former", "Current"], "Never")
    divider(c6)
    radio_row(c6, "Alcohol",   ["Never", "Occasional", "Regular"], "Occasional")
    divider(c6)
    radio_row(c6, "Exercise",  ["Sedentary", "Light", "Moderate", "Active"], "Light")
    divider(c6)
    radio_row(c6, "Diet type", ["Vegetarian", "Non-Veg", "Vegan"], "Vegetarian")

    # ════════════════════════════════════════════════════════════════════════
    #  SECTION 7 — VITALS LOG (last recorded)
    # ════════════════════════════════════════════════════════════════════════
    section(inner, "Vitals  (Last Recorded)", "📊")
    c7 = card(inner)

    vitals = [
        ("Blood Pressure",   "126 / 82 mmHg",  WARN),
        ("Blood Sugar (F)",  "118 mg/dL",       WARN),
        ("Cholesterol",      "172 mg/dL",       SAFE),
        ("Oxygen Saturation","98 %",            SAFE),
        ("Pulse",            "74 bpm",          SAFE),
        ("HbA1c",            "7.1 %",           WARN),
    ]

    for i, (vname, vval, vstatus) in enumerate(vitals):
        if i > 0:
            divider(c7)
        row = tk.Frame(c7, bg=CARD, pady=5)
        row.pack(fill="x")
        tk.Label(row, text=vname, font=FM(10),
                 bg=CARD, fg=TEXT_LIGHT, width=22, anchor="w").pack(side="left")
        tk.Label(row, text=vval, font=FM(11, "bold"),
                 bg=CARD, fg=TEXT_DARK).pack(side="left")

        dot_color = SAFE if vstatus == SAFE else WARN
        dot = tk.Canvas(row, width=10, height=10, bg=CARD, highlightthickness=0)
        dot.pack(side="right", padx=4)
        dot.create_oval(1, 1, 9, 9, fill=dot_color, outline="")

    # ════════════════════════════════════════════════════════════════════════
    #  SECTION 8 — CAREGIVER / EMERGENCY CONTACT
    # ════════════════════════════════════════════════════════════════════════
    section(inner, "Caregiver & Emergency Contact", "📞")
    c8 = card(inner)

    field_row(c8, "Caregiver name",     "Raj Sharma")
    divider(c8)
    field_row(c8, "Relation",           "Son")
    divider(c8)
    field_row(c8, "Phone",              "+91 98765 43210")
    divider(c8)
    field_row(c8, "Notify via",         "WhatsApp + SMS")
    divider(c8)
    field_row(c8, "Doctor name",        "Dr. Priya Nair")
    divider(c8)
    field_row(c8, "Doctor contact",     "+91 80 4321 0000")

    # ── Bottom padding ───────────────────────────────────────────────────────
    tk.Frame(inner, bg=BG, height=40).pack()

    return page


# ════════════════════════════════════════════════════════════════════════════
#  STANDALONE TEST — remove this block when integrating into your main app
# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    root.title("MediTrack — Medical History")
    root.geometry("900x700")
    root.configure(bg=BG)

    # Simulate your sidebar being 220px wide
    sidebar_stub = tk.Frame(root, bg="#2D7D6F", width=220)
    sidebar_stub.pack(side="left", fill="y")
    sidebar_stub.pack_propagate(False)
    tk.Label(sidebar_stub, text="← Sidebar here",
             bg="#2D7D6F", fg="white",
             font=tkfont.Font(family="Helvetica", size=10)).pack(pady=20)

    # Main area
    main = tk.Frame(root, bg=BG)
    main.pack(side="left", fill="both", expand=True)

    page = build_medical_history_page(main)
    page.pack(fill="both", expand=True)

    root.mainloop()