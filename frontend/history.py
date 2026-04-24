import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from frontend.sidebar import create_sidebar
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM 
from backend.db import getConnection
from frontend import session

def historypage(parent, controller):
    frame = Frame(parent, bg=BG)
    
    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    state = {"editing": False, "hasfilled": 0}
    labels = {}
    entries = {}

    def build_ui(status):
        for widget in container.winfo_children():
            widget.destroy()

        labels.clear()
        entries.clear()

        # SIDEBAR LOGIC: Version 1 - Only created if status is true
        if status == 1:
            sidebar = create_sidebar(container, controller, "Medical History")
            frame.sidebar = sidebar 
        else:
            frame.sidebar = None 

        right = Frame(container, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        con = scrollablefunc(right, BG)

        header = Frame(con, bg=BG)
        header.pack(fill="x", padx=20, pady=(20, 4))

        Label(header, text="Medical History", bg=BG, font=F(20, "bold"),
              fg=TEXT_DARK, anchor="w").pack(side="left")

        # ACTION BUTTON: "Save & Continue" for new users, "Edit" for existing
        btn_text = "Save & Continue" if status == 0 else "Edit"
        
        action_btn = Label(header, text=btn_text, font=FM(10, "bold"),
                         bg=ACCENT if status == 1 else ACCENT2, 
                         fg="white", padx=15, pady=8, cursor="hand2")
        action_btn.pack(side="right")
        action_btn.bind("<Button-1>", lambda e: toggle_mode(e, action_btn))

        schema = [
            {
                "section": "Personal Information",
                "fields": [
                    ("Name", "name", "entry"), ("Age", "age", "entry"),
                    ("Blood Group", "blood_group", "entry"), ("Gender", "gender", "dropdown"),
                    ("Contact", "contact", "entry"), ("Alternate contact", "alt_contact", "entry"),
                    ("Height (in cm)", "height", "entry"), ("Weight (in kg)", "weight", "entry")
                ]
            },
            {
                "section": "Health Details",
                "fields": [
                    ("Existing Conditions", "conditions", "text"),
                    ("Allergies", "allergies", "text"),
                    ("Past Surgeries", "surgeries", "text")
                ]
            }
        ]

        for section_data in schema:
            Label(con, text=section_data["section"], font=FM(12, "bold"),
                  bg=BG, fg=ACCENT).pack(anchor="w", padx=30, pady=(20, 5))
            Frame(con, height=1, bg="#EEE", width=600).pack(anchor="w", padx=30, fill="x")

            for label_text, data_key, input_type in section_data["fields"]:
                row = Frame(con, bg=BG, pady=10)
                row.pack(fill="x", padx=30)

                Label(row, text=label_text, font=FM(10), bg=BG, fg=TEXT_MED,
                      anchor="w", width=18).pack(side="left")

                input_cont = Frame(row, bg=BG)
                input_cont.pack(side="left", fill="x", expand=True)

                lbl_val = Label(input_cont, text="—", font=FM(11), bg=CARD,
                                fg=TEXT_DARK, anchor="w",
                                height=3 if input_type == "text" else 1,
                                padx=10, pady=8, highlightthickness=1, 
                                highlightbackground="#D8EAE7")
                lbl_val.pack(fill="x")
                labels[data_key] = lbl_val

                if input_type == "entry":
                    ent = Entry(input_cont, font=FM(11), bg="white", relief="flat",
                                highlightthickness=1, highlightbackground=ACCENT)
                    entries[data_key] = ent
                elif input_type == "dropdown":
                    cb = ttk.Combobox(input_cont, values=["Male", "Female", "Other"], 
                                      state="readonly", font=FM(11))
                    entries[data_key] = cb
                else:
                    txt = Text(input_cont, height=4, font=FM(11), bg="white",
                               relief="flat", highlightthickness=1,
                               highlightbackground=ACCENT, padx=5, pady=5)
                    entries[data_key] = txt

        load_data()

        # INITIAL STATE: If status is 0, force editing mode immediately
        if status == 0:
            state["editing"] = False
            toggle_mode(edit_btn=action_btn) 

        if hasattr(frame, "sidebar") and frame.sidebar and hasattr(frame.sidebar, "refresh"):
            frame.sidebar.refresh()

    def save_to_db():
        pid = session.patientid
        data = {k: (v.get().strip() if isinstance(v, (Entry, ttk.Combobox)) 
                else v.get("1.0", END).strip()) for k, v in entries.items()}
        
        # Simple Validation
        if not data.get("name") or not data.get("age"):
            messagebox.showwarning("Required", "Please fill in Name and Age atleast.")
            return False

        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT 1 FROM medical_history WHERE patient_id = %s", (pid,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO medical_history (patient_id) VALUES (%s)", (pid,))
            
            cursor.execute("""
                UPDATE medical_history SET
                name=%s, age=%s, blood_group=%s, gender=%s, contact=%s, 
                alt_contact=%s, height=%s, weight=%s, conditions=%s, 
                allergies=%s, surgeries=%s WHERE patient_id = %s
            """, (*data.values(), pid))
            conn.commit()

            if not state["hasfilled"]:
                cursor.execute("UPDATE patientinfo SET history_filled = 1 WHERE id = %s", (pid,))
                conn.commit()
                messagebox.showinfo("Success", "Profile Saved!")
                controller("dashboard") # Version 1 Goal: Redirect to finish onboarding
            else:
                messagebox.showinfo("Success", "Updated!")
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            if conn: conn.close()

    def load_data():
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM medical_history WHERE patient_id=%s", (session.patientid,))
            row = cursor.fetchone()
            if row:
                for key in labels:
                    val = row.get(key, "")
                    labels[key].config(text=val if val else "—")
        except: pass
        finally:
            if conn: conn.close()

    def toggle_mode(e=None, edit_btn=None):
        target_btn = e.widget if e else edit_btn
        if not state["editing"]:
            for key in entries:
                txt_val = labels[key].cget("text")
                if txt_val == "—": txt_val = ""
                labels[key].pack_forget()
                if isinstance(entries[key], (Entry, ttk.Combobox)):
                    if isinstance(entries[key], Entry):
                        entries[key].delete(0, END)
                        entries[key].insert(0, txt_val)
                    else: entries[key].set(txt_val)
                    entries[key].pack(fill="x", ipady=4)
                else:
                    entries[key].delete("1.0", END)
                    entries[key].insert("1.0", txt_val)
                    entries[key].pack(fill="x")
            
            # Label remains "Save & Continue" for first timers, or "Save" for editors
            if state["hasfilled"]:
                target_btn.config(text="Save", bg=ACCENT2)
            state["editing"] = True
        else:
            if save_to_db():
                for key in entries:
                    val = (entries[key].get() if isinstance(entries[key], (Entry, ttk.Combobox))
                           else entries[key].get("1.0", END).strip())
                    entries[key].pack_forget()
                    labels[key].config(text=val if val else "—")
                    labels[key].pack(fill="x")
                if target_btn: target_btn.config(text="Edit", bg=ACCENT)
                state["editing"] = False

    def refresh():
        pid = session.patientid
        current_status = 0
        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT history_filled FROM patientinfo WHERE id = %s", (pid,))
            res = cursor.fetchone()
            if res: current_status = res['history_filled']
        except: pass
        finally:
            if conn: conn.close()
        state["hasfilled"] = current_status
        build_ui(current_status)

    frame.refresh = refresh
    return frame