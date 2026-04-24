from tkinter import *
from tkinter import messagebox
from backend.db import getConnection
from config import CARD, ACCENT, TEXT_MED, FM
from frontend import session
from backend.mapping import medicine_name_mapping


def add_medicine_popup(add_card):
    popup = Toplevel()
    popup.title("Add Medicine")
    popup.geometry("300x150")
    popup.resizable(False, False)
    popup.configure(bg=CARD)

    popup.update_idletasks()
    x = (popup.winfo_screenwidth()  - 300) // 2
    y = (popup.winfo_screenheight() - 150) // 2
    popup.geometry(f"300x150+{x}+{y}")

    Label(popup, text="Medicine Name", font=FM(10),
          bg=CARD, fg=TEXT_MED).pack(anchor="w", padx=24, pady=(20, 4))

    name_var = StringVar()
    Entry(popup, textvariable=name_var, font=FM(11), width=28,
          bg="#F5F5F5", relief="flat", bd=0,
          highlightthickness=1, highlightbackground="#DDD",
          highlightcolor=ACCENT).pack(ipady=7, padx=24)

    def confirm():
        name = name_var.get().strip().title()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a medicine name")
            return

        conn = cursor = None
        try:
            conn   = getConnection()
            cursor = conn.cursor()

            # duplicate check
            cursor.execute(
                "SELECT * FROM medicines WHERE patient_id = %s AND LOWER(medicine_name) = LOWER(%s)",
                (session.patientid, name)
            )
            if cursor.fetchone():
                messagebox.showwarning("Duplicate", f"{name} already exists")
                return

            display_name = medicine_name_mapping(name)

            cursor.execute(
                    "INSERT INTO medicines (patient_id, medicine_name, status) VALUES (%s, %s, 'current')",
                     (session.patientid, display_name)
                        )
            conn.commit()

            messagebox.showinfo("Success", f"{display_name} added successfully!")
            add_card(display_name, active=True)
            popup.destroy()

        except Exception as e:
            messagebox.showerror("Database error", str(e))
        finally:
            if cursor: cursor.close()
            if conn:   conn.close()

    add_btn = Label(popup, text="Add", font=FM(10, "bold"),
                    bg=ACCENT, fg="white", padx=14, pady=7, cursor="hand2")
    add_btn.pack(anchor="e", padx=24, pady=(12, 0))
    add_btn.bind("<Button-1>", lambda e: confirm())
    popup.bind("<Return>", lambda e: confirm())

    return popup