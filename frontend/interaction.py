from tkinter import *
from tkinter import messagebox

from frontend.sidebar import create_sidebar
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, TEXT_DARK, TEXT_MED, DANGER, F, FM
from frontend import session

from backend.risk_logic import analyze_interactions

def interactionpage(parent, controller):

    frame = Frame(parent, bg=BG)

    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    sidebar = create_sidebar(container, controller, "Interactions")
    frame.sidebar = sidebar

    main_content = Frame(container, bg=BG)
    main_content.pack(side="left", fill="both", expand=True)

    con = scrollablefunc(main_content, BG)

    Label(con, text="Interactions", bg=BG, font=F(20, "bold"),
          fg=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 4))

    Label(con, text="Interactions among the medicines you are taking",
          bg=BG, font=F(13), fg=TEXT_MED,
          anchor="w").pack(fill="x", padx=20)

    Frame(con, height=1, bg=ACCENT).pack(fill="x", padx=20, pady=10)

    disc = Frame(con, bg="#FFF8E1", pady=8, padx=16)
    disc.pack(fill="x", padx=20, pady=(0, 10))
    Label(disc,
          text="⚠  For informational purposes only. "
               "Always consult your doctor before making changes to your medicines.",
          font=FM(9), bg="#FFF8E1",
          wraplength=700, justify="left").pack(anchor="w")

    info_strip = Frame(con, bg=CARD, padx=20, pady=10,
                       highlightthickness=1, highlightbackground="#E0E0E0")
    info_strip.pack(fill="x", padx=20, pady=(0, 10))

    patient_name_var = StringVar(value="")
    conditions_var   = StringVar(value="")
    med_count_var    = StringVar(value="")

    Label(info_strip, textvariable=patient_name_var,
          font=FM(11, "bold"), bg=CARD, fg=TEXT_DARK).pack(side="left")
    Label(info_strip, textvariable=conditions_var,
          font=FM(10), bg=CARD, fg=TEXT_MED).pack(side="left", padx=14)
    Label(info_strip, textvariable=med_count_var,
          font=FM(10, "bold"), bg=CARD, fg=ACCENT).pack(side="right")

    interaction_list = Frame(con, bg=BG)
    interaction_list.pack(fill="both", expand=True, padx=20, pady=10)

    def create_interaction_card(parent, med1, med2, severity,
                                 layman_desc, scientific_info,
                                 risk_score=-1, source=""):

        card = Frame(parent, bg=CARD, padx=15, pady=15,
                     highlightthickness=1, highlightbackground="#E0E0E0")
        card.pack(fill="x", pady=8)

        top_row = Frame(card, bg=CARD)
        top_row.pack(fill="x")

        Label(top_row, text=f"{med1} + {med2}",
              font=FM(12, "bold"), bg=CARD, fg=TEXT_DARK).pack(side="left")

        # Severity Color Logic (same as Labdhi's)
        if severity.lower() == "high":
            sev_color = DANGER
            sev_bg    = "#FDEDEC"
        elif severity.lower() == "moderate":
            sev_color = "#F39C12"
            sev_bg    = "#FEF5E7"
        else:
            sev_color = "#27AE60"
            sev_bg    = "#EAFAF1"

        Label(top_row, text=severity.upper(),
              font=FM(8, "bold"),
              bg=sev_bg, fg=sev_color,
              padx=10, pady=2).pack(side="left", padx=10)

        src_map = {
            "dataset_lookup": "Dataset",
            "shared_salt":    "Shared salt",
        }
        src_text = src_map.get(source, "")
        if src_text:
            Label(top_row, text=src_text, font=FM(8),
                  bg=CARD, fg=TEXT_MED).pack(side="right")

        if risk_score >= 0:
            bar_row = Frame(card, bg=CARD)
            bar_row.pack(fill="x", pady=(6, 0))

            Label(bar_row, text="Risk score:",
                  font=FM(9), bg=CARD, fg=TEXT_MED).pack(side="left")

            fill_w = int(min(risk_score, 1.0) * 160)

            Label(bar_row, text=f"{risk_score:.2f}",
                  font=FM(9, "bold"), bg=CARD,
                  fg=sev_color).pack(side="left", padx=4)

        Label(card, text=layman_desc,
              font=FM(10), bg=CARD, fg=TEXT_MED,
              wraplength=500, justify="left",
              pady=10).pack(fill="y", anchor="w")

        def show_scientific():
            messagebox.showinfo("Scientific Information", scientific_info)

        info_btn = Label(card, text="ⓘ Scientific Info",
                         font=FM(9, "bold"), bg=CARD,
                         fg=ACCENT, cursor="hand2")
        info_btn.pack(anchor="e")
        info_btn.bind("<Button-1>", lambda e: show_scientific())

    def refresh():
        # Clear old cards
        for w in interaction_list.winfo_children():
            w.destroy()

        try:
            patientid = session.patientid
            data    = analyze_interactions(patientid)

            # Fill patient info strip
            patient  = data.get("patient", {})
            name     = patient.get("name") or patient.get("username") or "Patient"
            age      = patient.get("age") or ""
            conds    = patient.get("conditions") or ""

            patient_name_var.set(
                f"👤  {name.title()}" + (f"  (Age {age})" if age else "")
            )
            conditions_var.set(
                conds[:55] + "…" if len(conds) > 55 else conds
                if conds else "No conditions recorded"
            )
            med_count_var.set(f"💊  {data['total_medicines']} medicine(s)")

            # No interactions case
            if not data["interactions"]:
                Label(interaction_list,
                      text="No interactions found between your current medicines.",
                      bg=BG, fg=TEXT_MED,
                      font=FM(11)).pack(pady=20)
                return

            # Create cards dynamically — same loop as Labdhi's original
            for item in data["interactions"]:

                med1     = item["medicine_1"]
                med2     = item["medicine_2"]
                severity = item["risk_level"]          # "HIGH" / "MODERATE" / "LOW"

                # Layman description (same format Labdhi's original used)
                layman_desc = (
                    f"Taking {med1} and {med2} together may increase risk due to "
                    + ", ".join(item["reasons"]) + "."
                )

                # Scientific info popup content
                scientific_info = (
                    f"Risk Score: {item['risk_score']}\n\n"
                    f"Reasons:\n- " + "\n- ".join(item["reasons"]) +
                    f"\n\nThis interaction is evaluated based on:\n"
                    f"• Salt composition similarity\n"
                    f"• Pharmacological pathway overlap (TF-IDF vectorisation)\n"
                    f"• Indian Medicine Dataset clinical records\n\n"
                    f"Source: {item.get('source', 'analysis engine')}"
                )

                create_interaction_card(
                    interaction_list,
                    med1, med2,
                    severity,
                    layman_desc,
                    scientific_info,
                    risk_score=item["risk_score"],
                    source=item.get("source", ""),
                )

        except Exception as e:
            Label(interaction_list,
                  text="Error loading interactions.",
                  bg=BG, fg="red",
                  font=FM(11)).pack(pady=20)
            print("Error:", e)

    frame.refresh = refresh
    print("LOGGED IN USER:", session.patientid)
    return frame