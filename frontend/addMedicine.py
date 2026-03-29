from tkinter import *
from tkinter import messagebox
from scrollable import scrollablefunc
from backend.db import getConnection
from config import CARD, ACCENT, TEXT_MED, FM
from frontend import session

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
        conn = getConnection()
        cursor = conn.cursor()

        name = name_var.get().strip()
        status = "current"
        id = session.patientid
        if name:
            # insert into db
            query = """ 
            INSERT INTO medicines (patient_id, name, status)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query,(id, name,status)) 
            conn.commit()                                       
            messagebox.showinfo("Success", f"{name} added successfully!")
            add_card(name, active=True)
            popup.destroy()

    add_btn = Label(popup, text="Add", font=FM(10, "bold"),
                    bg=ACCENT, fg="white", padx=14, pady=7, cursor="hand2")
    add_btn.pack(anchor="e", padx=24, pady=(12, 0))
    add_btn.bind("<Button-1>", lambda e: confirm())
    popup.bind("<Return>", lambda e: confirm())

    return popup