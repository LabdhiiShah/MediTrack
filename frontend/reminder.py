from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
from datetime import date, datetime, timedelta
from frontend.sidebar import create_sidebar
from frontend import session
from backend.db import getConnection
from config import BG, CARD, ACCENT, TEXT_DARK, TEXT_MED, TEXT_LIGHT, SECTION_BG, BORDER, SURFACE, ACCENT_DK, SAFE, DANGER, F, FM
from scrollable import scrollablefunc

TODAY_BLUE  = "#2E5BFF"
TAKEN_GREEN = "#2ECC71"
MISSED_RED  = DANGER
FUTURE_GREY = "#E0E0E0"

FREQ_OPTIONS = ["Daily (every 1 day)", "Every 2 days", "Every 3 days", "Weekly (every 7 days)", "Other…"]
FREQ_VALUES  = [1, 2, 3, 7, None]


def reminderpage(parent, controller):
    frame     = Frame(parent, bg=BG)
    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    frame.sidebar = create_sidebar(container, controller, "Reminders")

    def check_and_complete_schedules():
        """
        Runs on every load_reminders() call.
        - Finds any past scheduled day with no log → inserts 'missed' + extends end_date
        - Archives reminder only when end_date has fully passed and all days are logged
        NOTE: end_date is the ONLY source of extension.
              reminder_service.py must NOT extend end_date — only log missed.
        """
        today = datetime.now().date()
        conn  = getConnection()
        try:
            # active reminders
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT reminder_id, start_date, end_date, frequency, patient_id
                FROM   reminders
                WHERE  is_done = 0 AND patient_id = %s
            """, (session.patientid,))
            rows = cur.fetchall()

            for row in rows:
                r_id  = row['reminder_id']
                freq  = row['frequency'] or 1
                start = row['start_date']
                end   = row['end_date']   # may already be extended from previous runs

                # Build list of all scheduled days strictly before today. starts from start_date & build it till today
                scheduled_past = []
                current = start
                while current < today:
                    scheduled_past.append(current)
                    current += timedelta(days=freq)

                # Get all already-logged dates for this reminder
                cur.execute("""
                    SELECT logged_date FROM reminder_logs
                    WHERE  reminder_id = %s
                """, (r_id,))
                # logged_dates = {l['logged_date'] for l in cur.fetchall()}

                logged_dates = set()   # create empty set
                rows = cur.fetchall()  # fetch all records

                for l in rows:
                    logged_dates.add(l['logged_date'])

                # For every past scheduled day with no log → missed + extend
                for missed_d in sorted(scheduled_past):
                    if missed_d in logged_dates:
                        continue
                    if missed_d > end:
                        # Beyond current end_date — not yet a scheduled day
                        continue

                    cur.execute("""
                        INSERT IGNORE INTO reminder_logs
                            (reminder_id, patient_id, status, logged_date, logged_time)
                        VALUES (%s, %s, 'missed', %s, '00:00:00')
                    """, (r_id, row['patient_id'], missed_d))
                    #extend the end if 27dose is missed
                    end = end + timedelta(days=freq)
                    cur.execute(
                        "UPDATE reminders SET end_date = %s WHERE reminder_id = %s",
                        (end, r_id)
                    )
                    logged_dates.add(missed_d)   # prevent re-processing same date in loop
                    print(f"[maintenance] id={r_id} missed {missed_d} → end_date={end}")

                # Archive only when end_date is fully in the past
                if end < today:
                    cur.execute(
                        "UPDATE reminders SET is_done = 1 WHERE reminder_id = %s",
                        (r_id,)
                    )

            conn.commit()
        except Exception as e:
            print(f"Issue while checking doses in reminder {e}")
        finally:
            if conn: conn.close()

    def log_dose(r_id, status):
        """
        Logs today's dose as 'taken' or 'missed'.
        - 'missed'  → extends end_date by frequency
        - 'taken' on final day → archives reminder
        """
        today    = datetime.now().date()
        now_time = datetime.now().strftime("%H:%M:%S")
        conn = getConnection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                INSERT INTO reminder_logs
                    (reminder_id, patient_id, status, logged_date, logged_time)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    status      = VALUES(status),
                    logged_time = VALUES(logged_time)
            """, (r_id, session.patientid, status, today, now_time))

            cur.execute(
                "SELECT end_date, frequency FROM reminders WHERE reminder_id = %s",
                (r_id,)
            )
            res = cur.fetchone()

            if res:
                freq = res['frequency'] or 1
                if status == 'missed':
                    new_end = res['end_date'] + timedelta(days=freq)
                    cur.execute(
                        "UPDATE reminders SET end_date = %s WHERE reminder_id = %s",
                        (new_end, r_id)
                    )
                elif res['end_date'] <= today:
                    cur.execute(
                        "UPDATE reminders SET is_done = 1 WHERE reminder_id = %s",
                        (r_id,)
                    )

            conn.commit()
            load_reminders()
        except Exception as e:
            messagebox.showerror("Error", f"Could not log dose: {e}")
        finally:
            if conn: conn.close()

    def load_reminders():
        """Clears and reloads all reminder cards from DB."""
        check_and_complete_schedules()

        for w in today_list.winfo_children(): w.destroy()
        for w in past_list.winfo_children():  w.destroy()

        conn = getConnection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT * FROM reminders
                WHERE  patient_id = %s
                ORDER  BY is_done ASC, timing ASC
            """, (session.patientid,))
            rows = cur.fetchall()

            for row in rows:
                is_past      = (row['is_done'] == 1)
                target_frame = past_list if is_past else today_list

                cur.execute("""
                    SELECT logged_date, status
                    FROM   reminder_logs
                    WHERE  reminder_id = %s
                """, (row['reminder_id'],))
                logs = {l['logged_date']: l['status'] for l in cur.fetchall()}

                add_schedule_card(target_frame, row, logs, is_past)

            if not today_list.winfo_children():
                Label(today_list, text="No active reminders.", bg=BG,
                      fg=TEXT_LIGHT, font=F(10)).pack(pady=10, anchor="w")
            if not past_list.winfo_children():
                Label(past_list, text="No past schedules.", bg=BG,
                      fg=TEXT_LIGHT, font=F(10)).pack(pady=10, anchor="w")

        except Exception as e:
            print(f"[load_reminders] {e}")
        finally:
            if conn: conn.close()

    main_area = Frame(container, bg=BG)
    main_area.pack(side="left", fill="both", expand=True)

    header = Frame(main_area, bg=BG, padx=30, pady=20)
    header.pack(fill="x")

    title_v = Frame(header, bg=BG)
    title_v.pack(side="left")
    Label(title_v, text="Reminders",         font=F(22, "bold"), bg=BG, fg=TEXT_DARK).pack(anchor="w")
    Label(title_v, text="Never miss a dose", font=F(12),         bg=BG, fg=TEXT_MED ).pack(anchor="w")

    plus_btn = Label(header, text="+ Add Reminder", font=F(10, "bold"),
                     bg=ACCENT, fg="white", padx=15, pady=8, cursor="hand2")
    plus_btn.pack(side="right")
    plus_btn.bind("<Button-1>", lambda e: add_reminders_popup())

    scroll_content = scrollablefunc(main_area, BG)

    Label(scroll_content, text="Active Schedule", font=F(12, "bold"),
          bg=SECTION_BG, fg=ACCENT, anchor="w", padx=20, pady=10).pack(fill="x", padx=30, pady=(10, 0))
    today_list = Frame(scroll_content, bg=BG, padx=30)
    today_list.pack(fill="x")

    Label(scroll_content, text="Past Schedules", font=F(12, "bold"),
          bg="#F5F5F5", fg=TEXT_MED, anchor="w", padx=20, pady=10).pack(fill="x", padx=30, pady=(20, 0))
    past_list = Frame(scroll_content, bg=BG, padx=30)
    past_list.pack(fill="x")

    def add_schedule_card(parent, row, logs, is_past):
        today     = datetime.now().date()
        freq      = row.get('frequency', 1) or 1
        start     = row['start_date']
        end       = row['end_date']   # already extended — use this for dots

        card = Frame(parent, bg=CARD, padx=15, pady=12,
                     highlightthickness=1,
                     highlightbackground="#E0E0E0" if is_past else "#D8EAE7")
        card.pack(fill="x", pady=5)

        info = Frame(card, bg=CARD)
        info.pack(side="left", fill="x", expand=True)

        freq_label = f"Every {freq} day{'s' if freq > 1 else ''}"
        Label(info, text=row['medicine_name'], font=F(12, "bold"), bg=CARD,
              fg=TEXT_LIGHT if is_past else TEXT_DARK).pack(anchor="w")
        Label(info, text=f"{row['tablets']} tab  |  {row['timing']}  |  {freq_label}",
              font=F(9), bg=CARD, fg=TEXT_LIGHT).pack(anchor="w")

        if not is_past:
            circles_frame = Frame(info, bg=CARD)
            circles_frame.pack(anchor="w", pady=(5, 0))

            current = start
            while current <= end:
                status = logs.get(current)
                if status == 'taken':
                    color = TAKEN_GREEN
                elif status == 'missed' or (current < today and status is None):
                    color = MISSED_RED
                elif current == today:
                    color = TODAY_BLUE
                else:
                    color = FUTURE_GREY

                Label(circles_frame, text="●", font=("Arial", 12),
                      bg=CARD, fg=color).pack(side="left", padx=1)
                current += timedelta(days=freq)

            total_missed = sum(1 for s in logs.values() if s == 'missed')
            # Also count past scheduled days with no log at all
            d = start
            while d < today:
                if d <= end and logs.get(d) is None:
                    total_missed += 1
                d += timedelta(days=freq)

            if total_missed:
                Label(info, text=f"{total_missed} missed",
                      font=F(8), bg=CARD, fg=MISSED_RED).pack(anchor="w")
                
        actions = Frame(card, bg=CARD)
        actions.pack(side="right")

        if not is_past:
            today_status = logs.get(today)
            if today_status == 'taken':
                Label(actions, text="✓ Taken", font=F(9, "bold"),
                      bg=CARD, fg=TAKEN_GREEN).pack(side="left", padx=15)
            else:
                mark_lbl = Label(actions, text="Mark Taken", font=F(9, "bold"),
                                 bg=CARD, fg=ACCENT, cursor="hand2")
                mark_lbl.pack(side="left", padx=10)
                mark_lbl.bind("<Button-1>",
                              lambda e, rid=row['reminder_id']: log_dose(rid, 'taken'))

        del_btn = Label(actions, text="✕", font=F(10, "bold"),
                        bg=CARD, fg="#E74C3C", cursor="hand2")
        del_btn.pack(side="left", padx=5)
        del_btn.bind("<Button-1>",
                     lambda e, rid=row['reminder_id']: delete_reminder(rid))

    def add_reminders_popup():
        current_meds = get_medicines()
        if not current_meds:
            messagebox.showwarning("No Medicines",
                                   "Please add medicines in 'My Medicines' section first!")
            return

        popup = Toplevel(frame)
        popup.title("New Reminder")
        popup.geometry("430x660")
        popup.configure(bg=CARD)
        popup.grab_set()
        popup.update_idletasks()
        x = (popup.winfo_screenwidth()  - 430) // 2
        y = (popup.winfo_screenheight() - 660) // 2
        popup.geometry(f"+{x}+{y}")

        p_header = Frame(popup, bg=ACCENT, height=80)
        p_header.pack(fill="x")
        Label(p_header, text="Add Reminder", font=F(14, "bold"),
              bg=ACCENT, fg="white").place(x=24, y=20)

        body = Frame(popup, bg=CARD, padx=24, pady=10)
        body.pack(fill="both", expand=True)

        def s_label(t):
            Label(body, text=t, font=F(8, "bold"),
                  bg=CARD, fg=TEXT_LIGHT).pack(anchor="w", pady=(10, 2))

        # Medicine
        s_label("MEDICINE")
        med_name = StringVar(value=current_meds[0])
        Combobox(body, textvariable=med_name, values=current_meds,
                 state="readonly", font=F(11)).pack(fill="x")

        # Time
        s_label("TIME")
        time_row = Frame(body, bg=CARD)
        time_row.pack(anchor="w")
        hour_var, min_var = IntVar(value=8), IntVar(value=0)

        def create_spinner(parent, var, lo, hi):
            f   = Frame(parent, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
            f.pack(side="left", padx=2)
            up  = Label(f, text="▲", font=F(7), bg=SURFACE, cursor="hand2")
            lbl = Label(f, text=f"{var.get():02d}", font=("Courier New", 18, "bold"),
                        bg=SURFACE, width=3)
            dn  = Label(f, text="▼", font=F(7), bg=SURFACE, cursor="hand2")
            def upd(d):
                nv = var.get() + d
                nv = hi if nv < lo else (lo if nv > hi else nv)
                var.set(nv); lbl.config(text=f"{nv:02d}")
            up.pack(pady=(2, 0)); up.bind("<Button-1>", lambda e: upd(1))
            lbl.pack()
            dn.pack(pady=(0, 2)); dn.bind("<Button-1>", lambda e: upd(-1))

        create_spinner(time_row, hour_var, 1, 12)
        Label(time_row, text=":", font=F(16, "bold"), bg=CARD).pack(side="left", padx=5)
        create_spinner(time_row, min_var, 0, 59)

        ampm_var = StringVar(value="AM")
        ampm_btn = Label(time_row, text="AM", font=F(10, "bold"), bg=SURFACE, fg=ACCENT,
                         padx=10, pady=10,
                         highlightthickness=1, highlightbackground=BORDER, cursor="hand2")
        ampm_btn.pack(side="left", padx=10)
        ampm_btn.bind("<Button-1>", lambda e: [
            ampm_var.set("PM" if ampm_var.get() == "AM" else "AM"),
            ampm_btn.config(text=ampm_var.get())
        ])

        # Tablets
        s_label("NO. OF TABLETS")
        tab_var = IntVar(value=1)
        tab_f   = Frame(body, bg=CARD)
        tab_f.pack(anchor="w")

        def create_h_spinner(parent, var):
            f   = Frame(parent, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER)
            f.pack(side="left")
            lbl = Label(f, text=f"{var.get():02d}", font=("Courier New", 18, "bold"),
                        bg=SURFACE, width=3)
            def upd(d):
                nv = max(1, min(20, var.get() + d))
                var.set(nv); lbl.config(text=f"{nv:02d}")
            b1 = Label(f, text="◀", font=F(8), bg=SURFACE, cursor="hand2", padx=10)
            b1.pack(side="left"); b1.bind("<Button-1>", lambda e: upd(-1))
            lbl.pack(side="left")
            b2 = Label(f, text="▶", font=F(8), bg=SURFACE, cursor="hand2", padx=10)
            b2.pack(side="left"); b2.bind("<Button-1>", lambda e: upd(1))

        create_h_spinner(tab_f, tab_var)

        # Frequency
        s_label("FREQUENCY")
        freq_row   = Frame(body, bg=CARD)
        freq_row.pack(fill="x")
        freq_var   = StringVar(value=FREQ_OPTIONS[0])
        freq_combo = Combobox(freq_row, textvariable=freq_var,
                              values=FREQ_OPTIONS, state="readonly", font=F(11))
        freq_combo.pack(side="left", fill="x", expand=True)

        other_var   = IntVar(value=2)
        other_frame = Frame(body, bg=CARD)
        Label(other_frame, text="Every", font=F(10), bg=CARD,
              fg=TEXT_MED).pack(side="left", padx=(0, 5))
        Entry(other_frame, textvariable=other_var, font=F(11), width=4,
              justify="center", highlightthickness=1,
              highlightbackground=BORDER).pack(side="left")
        Label(other_frame, text="days", font=F(10), bg=CARD,
              fg=TEXT_MED).pack(side="left", padx=5)

        def on_freq_change(e=None):
            if freq_var.get() == "Other…":
                other_frame.pack(anchor="w", pady=(4, 0))
            else:
                other_frame.pack_forget()

        freq_combo.bind("<<ComboboxSelected>>", on_freq_change)

        # Date range
        s_label("DATE RANGE")
        dr = Frame(body, bg=CARD)
        dr.pack(fill="x")
        start_cal = DateEntry(dr, font=F(10), date_pattern='y-mm-dd')
        start_cal.pack(side="left", fill="x", expand=True, padx=2)
        end_cal   = DateEntry(dr, font=F(10), date_pattern='y-mm-dd')
        end_cal.pack(side="left", fill="x", expand=True, padx=2)

        def save_reminder():
            s_date = start_cal.get_date()
            e_date = end_cal.get_date()

            if s_date < datetime.now().date():
                messagebox.showerror("Error", "Start date cannot be in the past.")
                return
            if e_date < s_date:
                messagebox.showerror("Error", "End date must be after start date.")
                return

            sel      = freq_var.get()
            idx      = FREQ_OPTIONS.index(sel)
            freq_int = FREQ_VALUES[idx]
            if freq_int is None:
                try:
                    freq_int = int(other_var.get())
                    if freq_int < 1:
                        raise ValueError
                except (ValueError, TclError):
                    messagebox.showerror("Error", "Enter a valid number of days (≥ 1).")
                    return

            full_time = f"{hour_var.get():02d}:{min_var.get():02d} {ampm_var.get()}"
            conn = getConnection()
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO reminders
                        (patient_id, medicine_name, timing, tablets,
                         frequency, start_date, end_date, original_end_date, is_done)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0)
                """, (session.patientid, med_name.get(), full_time,
                      tab_var.get(), freq_int, s_date, e_date, e_date))
                conn.commit()
                popup.destroy()
                load_reminders()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))
            finally:
                if conn: conn.close()

        save_btn = Label(popup, text="Save Reminder", font=F(11, "bold"),
                         bg=ACCENT, fg="white", cursor="hand2", pady=12)
        save_btn.pack(fill="x", side="bottom", padx=24, pady=24)
        save_btn.bind("<Button-1>", lambda e: save_reminder())

    def delete_reminder(r_id):
        if messagebox.askyesno("Confirm Delete", "Remove this reminder?"):
            conn = getConnection()
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM reminder_logs WHERE reminder_id = %s", (r_id,))
                cur.execute("DELETE FROM reminders     WHERE reminder_id = %s", (r_id,))
                conn.commit()
                load_reminders()
            finally:
                if conn: conn.close()

    def get_medicines():
        conn = getConnection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT medicine_name FROM medicines WHERE patient_id = %s AND status = 'current'",
                (session.patientid,)
            )
            return [row['medicine_name'] for row in cur.fetchall()]
        finally:
            if conn: conn.close()

    frame.refresh = load_reminders
    frame.after(0, load_reminders)
    return frame