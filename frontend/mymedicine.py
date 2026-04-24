from tkinter import *
from tkinter import messagebox
from frontend.sidebar import create_sidebar
from frontend.addMedicine import add_medicine_popup   
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM, DANGER
from backend.db import getConnection
from frontend import session

SAFE = "#27AE60"

def mymedicinepage(parent, controller):

    frame = Frame(parent, bg=BG)

    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    frame.sidebar = create_sidebar(container, controller, "My Medicines")

    main = Frame(container, bg=BG)
    main.pack(side="left", fill="both", expand=True)

    # everywhere side="top" to ensure the it stacks tightly, as due to state change ui is getting disturbed
    # header
    Label(main, text="My Medicines", bg=BG, font=F(20, "bold"),
          fg=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 4))
    Label(main, text="Manage your current prescriptions", bg=BG, font=F(13),
          fg=TEXT_MED, anchor="w").pack(fill="x", padx=20)

    Frame(main, height=1, bg="#DDD8CC").pack(fill="x", pady=10)

    # + button
    plus_btn = Label(main, text="＋ Add Medicine", font=FM(10, "bold"),
                     bg=ACCENT, fg="white", padx=14, pady=8, cursor="hand2")
    plus_btn.pack(anchor="w", padx=32, pady=(12, 0))
    plus_btn.bind("<Button-1>", lambda e: add_medicine_popup(add_card))


    # Frame for all the medicines
    scrollable = Frame(main, bg=BG)
    scrollable.pack(fill="both",expand=True, padx=32, pady=10)

    allmedicines = scrollablefunc(scrollable,BG)

    # current section
    Label(allmedicines, text="Current Medicines", font=FM(12, "bold"),
          bg="#F0F7F5", fg=ACCENT, anchor="w",
          padx=20, pady=10).pack(fill="x")

    current_frame = Frame(allmedicines, bg=BG)
    current_frame.pack(fill="x",side="top")

    # past section
    past_label = Label(allmedicines, text="Past Medicines", font=FM(12, "bold"),
                       bg="#F0F7F5", fg=TEXT_MED, anchor="w",
                       padx=20, pady=10)
    past_label.pack(fill="x", pady=(10, 0))

    past_frame = Frame(allmedicines, bg=BG)
    past_frame.pack(fill="x",side="top")

    def refreshdata():
        patient_id = session.patientid
        try: 
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            # delete all existing UI
            for widget in current_frame.winfo_children():
                widget.destroy()
            for widget in past_frame.winfo_children():
                widget.destroy()

            # extract from db all medicines
            query = """SELECT * FROM medicines WHERE patient_id = %s"""
            cursor.execute(query,(patient_id,))
            medicines = cursor.fetchall()

            for med in medicines:
                medname = med['medicine_name']
                status = (med['status'] == 'current')
                add_card(medname, status)

        except Exception as e:
            messagebox.showerror("Database error","In refresh")

        finally:
            cursor.close()
            conn.close()

    def add_card(name, active=True):
        # place in correct section 
        parent_frame = current_frame if active else past_frame

        med = Frame(parent_frame, bg=CARD, padx=20, pady=12,
                    highlightthickness=1,
                    highlightbackground="#D8EAE7" if active else "#E0E0E0")
        med.pack(fill="x", pady=3)

        left = Frame(med, bg=CARD)
        left.pack(side="left", fill="x", expand=True)

        name_lbl = Label(left, text=name, font=FM(11), bg=CARD,
                         fg=TEXT_DARK if active else TEXT_LIGHT)
        name_lbl.pack(anchor="w")

        def delete_medicine():
            if messagebox.askyesno("Confirm",f"Delete {name} permanently"):
                try:
                    conn = getConnection()
                    cursor = conn.cursor()

                    deletequery = "DELETE FROM medicines WHERE patient_id = %s AND medicine_name = %s"
                    cursor.execute(deletequery,(session.patientid,name))
                    conn.commit()
                    med.destroy()
                    allmedicines.update_idletasks()

                except Exception as e:
                    messagebox.showerror("Database error","In deleting medicines")

                finally:
                    cursor.close()
                    conn.close()


        delete_lbl = Label(med,text="  Delete",font=FM(9, "bold"), bg=CARD,
                           fg=DANGER if active else ACCENT2,
                           cursor="hand2")
        delete_lbl.pack(side="right",anchor="n")
        delete_lbl.bind("<Button-1>", lambda e: delete_medicine())

        state = {"active": active}

        status_lbl = Label(med,
                           text="✓ Current" if active else "📦 Past",
                           font=FM(9, "bold"), bg=CARD,
                           fg=SAFE if active else TEXT_LIGHT,
                           cursor="hand2")
        status_lbl.pack(side="right", anchor="n")

        def toggle():
            patient_id = session.patientid

            state["active"] = not state["active"]
                
            newstatus = "current" if state["active"] else "past"

            try:
                conn = getConnection()
                cursor = conn.cursor()

                # change the state in db too
                changeStatusQuery = """UPDATE medicines SET status = %s WHERE patient_id = %s AND medicine_name = %s"""
                cursor.execute(changeStatusQuery, (newstatus, patient_id, name))
                conn.commit()

            except Exception as e:
                messagebox.showerror("DataBase error","In toggle")

            finally:
                cursor.close()
                conn.close()

            # destroy and recreate in correct section
            med.destroy()
            current_frame.update_idletasks()
            past_frame.update_idletasks()

            add_card(name, active=state["active"])


        status_lbl.bind("<Button-1>", lambda e: toggle())

    # will derieve from db all the existing medicines and based on status over there, will place in the frame
    frame.refresh = refreshdata

    return frame