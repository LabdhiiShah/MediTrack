import tkinter as tk
import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from frontend.sidebar import create_sidebar
from frontend import session
from backend.db import getConnection
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, TEXT_DARK, TEXT_MED, TEXT_LIGHT, F, FM

def profilepage(parent, controller):
    frame = Frame(parent, bg=BG)
    
    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    # Sidebar remains exactly where you put it
    frame.sidebar = create_sidebar(container, controller, "Profile")

    main = Frame(container, bg=BG)
    main.pack(side="left", fill="both", expand=True)

    header = Frame(main, bg=BG)
    header.pack(fill="x", padx=20, pady=(20, 10))

    Label(header, text="My Profile", bg=BG, font=F(20, "bold"), fg=TEXT_DARK).pack(side="left")

    editing = False
    field_widgets = [] 

    def savedata():
        for i, field in enumerate(field_widgets):
            val = field['entry'].get().strip()
            if not val or val == "-":
                field_names = ["Username", "E-mail", "Contact", "DOB"]
                messagebox.showwarning("Validation Error", f"The field '{field_names[i]}' cannot be empty.")
                return False

        try:
            patientid = session.patientid
            new_values = [
                field_widgets[0]['entry'].get().strip(),
                field_widgets[1]['entry'].get().strip(),
                field_widgets[2]['entry'].get().strip(),
                field_widgets[3]['entry'].get().strip(),
                patientid
            ]

            conn = getConnection()
            cursor = conn.cursor()
            
            query = "UPDATE patientinfo SET username=%s, email=%s, contact=%s, dob=%s WHERE id=%s"
            cursor.execute(query, new_values)
            conn.commit()
            return True
            
        except Exception as e:
            messagebox.showerror("Update Error", f"Failed to save to database: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                cursor.close()
                conn.close()

    def getdata():
        try:
            id = session.patientid
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username, email, contact, dob FROM patientinfo WHERE id = %s", (id,))
            row = cursor.fetchone()

            if row:
                db_keys = ['username', 'email', 'contact', 'dob']
                for i, key in enumerate(db_keys):
                    data = row.get(key)
                    
                    if data is None or str(data).strip().lower() in ["none", ""]:
                        clean_text = "-"
                    else:
                        clean_text = str(data)
                    
                    field_widgets[i]['label'].config(text=clean_text)
                    field_widgets[i]['entry'].delete(0, END)
                    field_widgets[i]['entry'].insert(0, "" if clean_text == "-" else clean_text)
            
        except Exception as e:
            print(f"Error retrieving profile: {e}")
        finally:
            if 'conn' in locals() and conn:
                cursor.close()
                conn.close()

    def toggle_edit():
        nonlocal editing
        if not editing:
            edit_btn.config(text="Save Changes", bg="#27AE60")
            for field in field_widgets:
                txt_val = field['label'].cget("text")
                if txt_val in ["—", "-"]: txt_val = ""
                field['entry'].delete(0, END)
                field['entry'].insert(0, txt_val)
                
                field['label'].pack_forget()
                field['entry'].pack(fill="x", ipady=7)
            editing = True
        else:
            mail = field_widgets[1]['entry'].get().strip()
            if not re.match(r"[^@]+@[^@]+\.[^@]+", mail):
                messagebox.showwarning("Invalid Email", "Please enter a valid email address")
                return
                
            if len(field_widgets[2]['entry'].get().strip()) != 10:
                messagebox.showwarning("Invalid Contact number", "Please enter a valid contact number")
                return
        
            if savedata(): 
                
                edit_btn.config(text="Edit Profile", bg=ACCENT)
                for field in field_widgets:
                    new_val = field['entry'].get().strip()
                    field['label'].config(text=new_val if new_val else "-")
                    
                    field['entry'].pack_forget()
                    field['label'].pack(fill="x")

                messagebox.showinfo("Success", "Profile Updated Successfully!")
                editing = False

    edit_btn = Label(header, text="Edit Profile", font=FM(10, "bold"),
                     bg=ACCENT, fg="white", padx=15, pady=8, cursor="hand2")
    edit_btn.pack(side="right")
    edit_btn.bind("<Button-1>", lambda e: toggle_edit())

    Frame(main, height=1, bg="#DDD8CC").pack(fill="x", padx=20, pady=5)

    con = scrollablefunc(main, BG)
    content = Frame(con, bg=BG)
    content.pack(fill="both", expand=True, padx=20, pady=10)

    def create_profile_row(text, default_value):
        row = Frame(content, bg=BG, pady=10) 
        row.pack(fill="x")

        Label(row, text=text, font=FM(10), fg=TEXT_MED, bg=BG, width=18, anchor="w").pack(side="left")

        input_frame = Frame(row, bg=BG)
        input_frame.pack(side="left", fill="x", expand=True)

        display_lbl = Label(input_frame, text=default_value, 
                            font=FM(11), fg=TEXT_DARK, bg=CARD, 
                            anchor="w", padx=10, pady=8, 
                            height=1, 
                            highlightthickness=1, 
                            highlightbackground="#D8EAE7")
        display_lbl.pack(fill="x")

        entry = Entry(input_frame, font=FM(11), fg=TEXT_DARK, bg="white", 
                      relief="flat", highlightthickness=1, 
                      highlightbackground=ACCENT)
        entry.insert(0, "" if default_value == "-" else default_value)
        entry.pack_forget()

        field_widgets.append({'label': display_lbl, 'entry': entry})

    create_profile_row("Username", "-")
    create_profile_row("E-mail id", "-")
    create_profile_row("Contact", "-")
    create_profile_row("DOB", "-")

    frame.refresh = getdata
    getdata()

    return frame