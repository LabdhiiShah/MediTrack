# from tkinter import *
# from frontend.sidebar import create_sidebar
# from scrollable import scrollablefunc
# from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM

# def mymedicinepage(parent,controller):
#     frame = Frame(parent,bg=BG)

#     container = Frame(frame,bg=BG)
#     container.pack(fill="both",expand=True)
    
#     create_sidebar(container, controller, "My Medicines")

#     main = Frame(container, bg=BG)
#     main.pack(side="left",fill="both",expand=True)

#     Label(main,text="My Medicines",bg=BG,font=F(20,"bold"),anchor="w").pack(fill="x",padx=20, pady=(20, 4))
#     Label(main,text="Manage your current prescriptions",bg=BG,font=F(13),anchor="w").pack(fill="x",padx=20)

#     Frame(main,height=1,bg="#DDD8CC").pack(fill="x",pady=10)

#     allmedicines = Frame(main,bg=BG)
#     allmedicines.pack(fill="x",padx=32,pady=10)

#     Lcurrmed = Label(allmedicines, text="Current Medicines", font=FM(12, "bold"),
#                 bg="#F0F7F5" , fg=ACCENT, anchor="w", padx=20, pady=10)
#     Lcurrmed.pack(fill="x")

#     medicines = [
#         "Metformin",
#         "Amlodipine",
#         "Vitamin",
#         "Atorvastatin",
#         "Aspirin"
#     ]

#     # loop of labels of medicines
#     for name in medicines:
#         med = Frame(allmedicines, bg=CARD, padx=20,pady=12,
#                     highlightthickness=1,highlightbackground="#D8EAE7")
#         med.pack(fill="x",pady=3)

#         Label(med, text=name, font=FM(11),bg=CARD,fg=TEXT_DARK).pack(anchor="w")

#     def add_medicine_popup():
#         popup = Toplevel()
#         popup.title("Add Medicine")
#         popup.geometry("300x150")
#         popup.resizable(False, False)
#         popup.configure(bg=CARD)

#         # center popup
#         popup.update_idletasks()
#         x = (popup.winfo_screenwidth() - 300) // 2
#         y = (popup.winfo_screenheight() - 150) // 2
#         popup.geometry(f"300x150+{x}+{y}")

#         Label(popup, text="Medicine Name", font=FM(10),
#             bg=CARD, fg=TEXT_MED).pack(anchor="w", padx=24, pady=(20, 4))

#         name_var = StringVar()
#         Entry(popup, textvariable=name_var, font=FM(11), width=28,
#             bg="#F5F5F5", relief="flat", bd=0,
#             highlightthickness=1, highlightbackground="#DDD",
#             highlightcolor=ACCENT).pack(ipady=7, padx=24)

#         def confirm():
#             name = name_var.get().strip()
#             if name:
#                 med = Frame(allmedicines, bg=CARD, padx=20, pady=12,
#                             highlightthickness=1, highlightbackground="#D8EAE7")
#                 med.pack(fill="x", pady=3)
#                 Label(med, text=name, font=FM(11), bg=CARD, fg=TEXT_DARK).pack(anchor="w")
#                 popup.destroy()

#         add_btn = Label(popup, text="Add", font=FM(10, "bold"),
#                         bg=ACCENT, fg="white", padx=14, pady=7, cursor="hand2")
#         add_btn.pack(anchor="e", padx=24, pady=(12, 0))
#         add_btn.bind("<Button-1>", lambda e: confirm())
#         popup.bind("<Return>", lambda e: confirm())

#     # + button
#     plus_btn = Label(main, text="＋ Add Medicine", font=FM(10, "bold"),
#                     bg=ACCENT, fg="white", padx=14, pady=8, cursor="hand2")
#     plus_btn.pack(anchor="w", padx=32, pady=(12, 0))
#     plus_btn.bind("<Button-1>", lambda e: add_medicine_popup())

#     return frame

from tkinter import *
from frontend.sidebar import create_sidebar
from frontend.addMedicine import add_medicine_popup   
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM

SAFE = "#27AE60"

def mymedicinepage(parent, controller):
    frame = Frame(parent, bg=BG)

    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    create_sidebar(container, controller, "My Medicines")

    main = Frame(container, bg=BG)
    main.pack(side="left", fill="both", expand=True)

    # header
    Label(main, text="My Medicines", bg=BG, font=F(20, "bold"),
          fg=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 4))
    Label(main, text="Manage your current prescriptions", bg=BG, font=F(13),
          fg=TEXT_MED, anchor="w").pack(fill="x", padx=20)

    Frame(main, height=1, bg="#DDD8CC").pack(fill="x", pady=10)

    allmedicines = Frame(main, bg=BG)
    allmedicines.pack(fill="x", padx=32, pady=10)

    # current section
    Label(allmedicines, text="Current Medicines", font=FM(12, "bold"),
          bg="#F0F7F5", fg=ACCENT, anchor="w",
          padx=20, pady=10).pack(fill="x")

    current_frame = Frame(allmedicines, bg=BG)
    current_frame.pack(fill="x")

    # past section
    past_label = Label(allmedicines, text="Past Medicines", font=FM(12, "bold"),
                       bg="#F0F7F5", fg=TEXT_MED, anchor="w",
                       padx=20, pady=10)
    past_label.pack(fill="x", pady=(10, 0))

    past_frame = Frame(allmedicines, bg=BG)
    past_frame.pack(fill="x")

    medicines = ["Metformin", "Amlodipine", "Vitamin", "Atorvastatin", "Aspirin"]

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

        state = {"active": active}

        status_lbl = Label(med,
                           text="✓ Current" if active else "📦 Past",
                           font=FM(9, "bold"), bg=CARD,
                           fg=SAFE if active else TEXT_LIGHT,
                           cursor="hand2")
        status_lbl.pack(side="right", anchor="n")

        def toggle():
            state["active"] = not state["active"]
            # destroy and recreate in correct section
            med.destroy()
            add_card(name, active=state["active"])

        status_lbl.bind("<Button-1>", lambda e: toggle())

    for name in medicines:
        add_card(name)

    # popup
    

    # + button
    plus_btn = Label(main, text="＋ Add Medicine", font=FM(10, "bold"),
                     bg=ACCENT, fg="white", padx=14, pady=8, cursor="hand2")
    plus_btn.pack(anchor="w", padx=32, pady=(12, 0))
    plus_btn.bind("<Button-1>", lambda e: add_medicine_popup(add_card))

    return frame