from tkinter import *
from datetime import datetime, date, timedelta
import math

from frontend.sidebar import create_sidebar
from frontend import session
from backend.db import getConnection
from config import (BG, CARD, ACCENT, TEXT_DARK, TEXT_MED, TEXT_LIGHT,
                    SECTION_BG, BORDER, SURFACE, DANGER, SAFE, F, FM)
from scrollable import scrollablefunc

GREEN  = "#2ECC71"
RED    = DANGER
YELLOW = "#F39C12"


def dashboardpage(parent, controller):
    frame     = Frame(parent, bg=BG)
    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    frame.sidebar = create_sidebar(container, controller, "Dashboard")

    main_area = Frame(container, bg=BG)
    main_area.pack(side="left", fill="both", expand=True)

    scroll_content = scrollablefunc(main_area, BG)

    # header
    header = Frame(scroll_content, bg=BG, padx=30, pady=20)
    header.pack(fill="x")

    title_v = Frame(header, bg=BG)
    title_v.pack(side="left")
    Label(title_v, text="Dashboard", font=F(22, "bold"),
          bg=BG, fg=TEXT_DARK).pack(anchor="w")
    date_lbl = Label(title_v, text="", font=F(11), bg=BG, fg=TEXT_MED)
    date_lbl.pack(anchor="w")

    #row - missed reminders
    row1 = Frame(scroll_content, bg=BG, padx=30)
    row1.pack(fill="x", pady=(0, 12))
    row1.grid_columnconfigure(0, weight=1)
    row1.grid_columnconfigure(1, weight=1)

    def card(parent, col):
        c = Frame(parent, bg=CARD, padx=20, pady=18,
                  highlightthickness=1, highlightbackground="#E0E0E0")
        c.grid(row=0, column=col, sticky="nsew",
               padx=(0, 8) if col == 0 else (8, 0))
        return c

    # next Reminder
    upcoming_reminder = card(row1, 0)
    Label(upcoming_reminder, text="Next Reminder", font=F(9, "bold"),
          bg=CARD, fg=TEXT_MED).pack(anchor="w")
    next_med_lbl  = Label(upcoming_reminder, text="—", font=F(16, "bold"),
                           bg=CARD, fg=TEXT_DARK)
    next_med_lbl.pack(anchor="w", pady=(6, 0))
    next_time_lbl = Label(upcoming_reminder, text="", font=F(11), bg=CARD, fg=TEXT_MED)
    next_time_lbl.pack(anchor="w")
    next_tab_lbl  = Label(upcoming_reminder, text="", font=F(9),  bg=CARD, fg=TEXT_MED)
    next_tab_lbl.pack(anchor="w", pady=(2, 0))
    next_badge    = Label(upcoming_reminder, text="", font=F(9, "bold"),
                           bg=CARD, fg=ACCENT)
    next_badge.pack(anchor="w", pady=(8, 0))

    # missed doses
    missed_dose = card(row1, 1)
    Label(missed_dose, text="Missed Doses This Week", font=F(9, "bold"),
          bg=CARD, fg=TEXT_MED).pack(anchor="w")
    missed_count_lbl = Label(missed_dose, text="0", font=F(34, "bold"),
                              bg=CARD, fg=TEXT_DARK)
    missed_count_lbl.pack(anchor="w", pady=(4, 0))
    Label(missed_dose, text="doses missed", font=F(10),
          bg=CARD, fg=TEXT_MED).pack(anchor="w")
    missed_list_frame = Frame(missed_dose, bg=CARD)
    missed_list_frame.pack(anchor="w", fill="x", pady=(10, 0))

    # donut & quick stats
    row2 = Frame(scroll_content, bg=BG, padx=30)
    row2.pack(fill="x", pady=(0, 12))

    c_stats = Frame(row2, bg=CARD, padx=24, pady=20,
                    highlightthickness=1, highlightbackground="#E0E0E0")
    c_stats.pack(fill="x")

    Label(c_stats, text="Quick Stats", font=F(11, "bold"),
          bg=CARD, fg=TEXT_DARK).pack(anchor="w", pady=(0, 14))

    stats_body = Frame(c_stats, bg=CARD)
    stats_body.pack(fill="x")

    # Left: stat rows
    stats_left = Frame(stats_body, bg=CARD)
    stats_left.pack(side="left", fill="y", padx=(0, 0))

    def stat_row(parent, label_text):
        box = Frame(parent, bg=CARD)
        box.pack(anchor="w", pady=5)
        Label(box, text=label_text, font=F(10), bg=CARD,
              fg=TEXT_MED, width=18, anchor="w").pack(side="left")
        val = Label(box, text="—", font=F(11, "bold"), bg=CARD, fg=TEXT_DARK)
        val.pack(side="left", padx=(6, 0))
        return val

    today_val_lbl = stat_row(stats_left, "Today taken")
    week_val_lbl  = stat_row(stats_left, "Missed this week")
    med_val_lbl   = stat_row(stats_left, "Active medicines")

    # Divider
    Frame(stats_body, bg="#E8E8E8", width=1).pack(
        side="left", fill="y", padx=30, pady=4)

    # Right: donut chart
    stats_right = Frame(stats_body, bg=CARD)
    stats_right.pack(side="left", fill="both", expand=True)

    Label(stats_right, text="Weekly Adherence", font=F(9, "bold"),
          bg=CARD, fg=TEXT_MED).pack(anchor="w", pady=(0, 10))

    # donut_row = Frame(stats_right, bg=CARD)
    # donut_row.pack(anchor="w")

    # donut_canvas = Canvas(donut_row, width=110, height=110,
    #                       bg=CARD, highlightthickness=0)
    # donut_canvas.pack(side="left")

    # donut_info = Frame(stats_right, bg=CARD)
    # donut_info.pack(side="left", padx=(18, 0), anchor="center")

    adh_pct_lbl    = Label(stats_right, text="—%", font=F(22, "bold"),
                            bg=CARD, fg=TEXT_DARK)
    adh_pct_lbl.pack(anchor="w", pady=(0, 10))
    Label(stats_right, text="adherence", font=F(9),
          bg=CARD, fg=TEXT_MED).pack(anchor="w", pady=(0, 10))
    adh_taken_lbl  = Label(stats_right, text="", font=F(9), bg=CARD, fg=TEXT_MED)
    adh_taken_lbl.pack(anchor="w", pady=(8, 0))
    adh_missed_lbl = Label(stats_right, text="", font=F(9), bg=CARD, fg=TEXT_MED)
    adh_missed_lbl.pack(anchor="w")

    def draw_donut(pct):
        donut_canvas.delete("all")
        cx, cy = 55, 55
        r_out, r_in = 46, 30
        track_color = "#EEEEEE"
        fill_color  = GREEN if pct >= 80 else (YELLOW if pct >= 50 else RED)

        # Track
        donut_canvas.create_arc(
            cx - r_out, cy - r_out, cx + r_out, cy + r_out,
            start=0, extent=359.99,
            outline=track_color, width=r_out - r_in, style="arc"
        )
        # Fill
        if pct > 0:
            extent = (pct / 100) * 359.99
            donut_canvas.create_arc(
                cx - r_out, cy - r_out, cx + r_out, cy + r_out,
                start=90, extent=-extent,
                outline=fill_color, width=r_out - r_in, style="arc"
            )
        # Center label
        donut_canvas.create_text(
            cx, cy, text=f"{pct}%",
            font=("Arial", 11, "bold"), fill=TEXT_DARK
        )

    # active
    row3 = Frame(scroll_content, bg=BG, padx=30)
    row3.pack(fill="x", pady=(0, 24))

    c_meds = Frame(row3, bg=CARD, padx=24, pady=20,
                   highlightthickness=1, highlightbackground="#E0E0E0")
    c_meds.pack(fill="x")

    Label(c_meds, text="Active Medicines", font=F(11, "bold"),
          bg=CARD, fg=TEXT_DARK).pack(anchor="w", pady=(0, 10))

    meds_list_frame = Frame(c_meds, bg=CARD)
    meds_list_frame.pack(fill="x")

    # refresh
    def refresh():
        #date time
        today = datetime.now()
        today_date = today.date()

        date_lbl.config(text=today.strftime("%A, %d %B %Y"))
        # db connections
        conn = getConnection()
        try:
            cur = conn.cursor(dictionary=True)

            # get active medicines from db
            cur.execute("""
                SELECT medicine_name FROM medicines
                WHERE patient_id = %s AND status = 'current'
            """, (session.patientid,))
            active_meds = [r['medicine_name'] for r in cur.fetchall()]
            # count medicines
            med_val_lbl.config(text=str(len(active_meds)))

            # medicines list
            for w in meds_list_frame.winfo_children():
                w.destroy()
            for i, m in enumerate(active_meds):
                row_bg = SECTION_BG if i % 2 == 0 else CARD
                r = Frame(meds_list_frame, bg=row_bg, padx=12, pady=8)
                r.pack(fill="x")
                Label(r, text=m, font=F(10), bg=row_bg,
                      fg=TEXT_DARK).pack(side="left")
            if not active_meds:
                Label(meds_list_frame, text="No active medicines.",
                      font=F(10), bg=CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=6)

            # active reminders
            cur.execute("""
                SELECT reminder_id, medicine_name, timing,
                       tablets, frequency, start_date, end_date
                FROM   reminders
                WHERE  patient_id = %s AND is_done = 0
                ORDER  BY timing ASC
            """, (session.patientid,))
            reminders = cur.fetchall()
            # checks if reminder for today is there not
            def is_scheduled(rem):
                freq  = rem.get('frequency', 1) or 1
                start = rem['start_date']
                end   = rem['end_date']
                if not (start <= today_date <= end):
                    return False
                return (today_date - start).days % freq == 0

            scheduled_today = [r for r in reminders if is_scheduled(r)]

            cur.execute("""
                SELECT reminder_id, status FROM reminder_logs
                WHERE  patient_id = %s AND logged_date = %s
            """, (session.patientid, today_date))
            today_logs = {r['reminder_id']: r['status'] for r in cur.fetchall()}

            taken_today = sum(1 for r in scheduled_today
                              if today_logs.get(r['reminder_id']) == 'taken')
            total_today = len(scheduled_today)
            today_val_lbl.config(text=f"{taken_today} / {total_today}")

            # Next reminder
            def parse_time(t):
                for fmt in ("%I:%M %p", "%I:%M%p", "%H:%M"):
                    try:
                        return datetime.strptime(t.strip(), fmt).replace(
                            year=today.year, month=today.month, day=today.day)
                    except:
                        pass
                return None

            future = []
            for r in scheduled_today:
                if today_logs.get(r['reminder_id']) == 'taken':
                    continue
                dt = parse_time(r['timing'])
                if dt and dt > today:
                    future.append((dt, r))

            if future:
                future.sort(key=lambda x: x[0])
                ndt, nr = future[0]
                mins_left = int((ndt - today).total_seconds() / 60)
                next_med_lbl.config(text=nr['medicine_name'])
                next_time_lbl.config(text=ndt.strftime("%I:%M %p"))
                next_tab_lbl.config(text=f"{nr['tablets']} tablet(s)")
                if mins_left < 60:
                    next_badge.config(text=f"In {mins_left} min", fg=RED)
                else:
                    next_badge.config(
                        text=f"In {mins_left // 60}h {mins_left % 60}m",
                        fg=ACCENT)
            else:
                not_taken = [r for r in scheduled_today
                             if today_logs.get(r['reminder_id']) != 'taken']
                if not_taken:
                    next_med_lbl.config(text=not_taken[0]['medicine_name'])
                    next_time_lbl.config(text=not_taken[0]['timing'])
                    next_tab_lbl.config(text=f"{not_taken[0]['tablets']} tablet(s)")
                    next_badge.config(text="Not yet taken", fg=YELLOW)
                else:
                    next_med_lbl.config(text="All done for today")
                    next_time_lbl.config(text="")
                    next_tab_lbl.config(text="")
                    next_badge.config(text="Great job!", fg=GREEN)

            # Missed this week
            week_start = today_date - timedelta(days=today_date.weekday())
            cur.execute("""
                SELECT rl.reminder_id, rl.logged_date, rl.status,
                       r.medicine_name
                FROM   reminder_logs rl
                JOIN   reminders r ON rl.reminder_id = r.reminder_id
                WHERE  rl.patient_id = %s
                  AND  rl.logged_date >= %s
                  AND  rl.logged_date <= %s
            """, (session.patientid, week_start, today_date))
            week_logs = cur.fetchall()

            missed_week = [l for l in week_logs if l['status'] == 'missed']
            missed_count_lbl.config(
                text=str(len(missed_week)),
                fg=RED if missed_week else GREEN
            )
            week_val_lbl.config(text=str(len(missed_week)))

            # Medicines list
            for w in meds_list_frame.winfo_children():
                w.destroy()

            for m in active_meds:
                # Set row_bg to a single color (CARD) to remove alternating logic
                row_bg = CARD 
                r = Frame(meds_list_frame, bg=row_bg, padx=12, pady=8)
                r.pack(fill="x")
                Label(r, text=m, font=F(10), bg=row_bg,
                      fg=TEXT_DARK).pack(side="left")

            if not active_meds:
                Label(meds_list_frame, text="No active medicines.",
                      font=F(10), bg=CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=6)

            # Adherence + donut
            total_week = len(week_logs)
            taken_week = sum(1 for l in week_logs if l['status'] == 'taken')
            adh_pct    = int((taken_week / total_week) * 100) if total_week else 100

            adh_color = GREEN if adh_pct >= 80 else (YELLOW if adh_pct >= 50 else RED)
            adh_pct_lbl.config(text=f"{adh_pct}%", fg=adh_color)
            adh_taken_lbl.config(text=f"Taken:   {taken_week}")
            adh_missed_lbl.config(text=f"Missed:  {total_week - taken_week}")
            # draw_donut(adh_pct)

        except Exception as e:
            print(f"[dashboard] refresh error: {e}")
        finally:
            if conn: conn.close()

    frame.refresh = refresh
    frame.after(0, refresh)
    return frame