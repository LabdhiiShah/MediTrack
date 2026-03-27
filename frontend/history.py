from tkinter import *
from frontend.sidebar import create_sidebar
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM 

def historypage(parent,controller):
    frame = Frame(parent, bg=BG)
    # user = controller.currentUser

    container = Frame(frame,bg=BG)
    container.pack(fill="both",expand=True)

    # if user["history_filled"]:
    #     create_sidebar(container, controller, "Medical History")
    
    create_sidebar(container, controller, "Medical History")
    
    right = Frame(container, bg=BG)
    right.pack(side="left",fill="both",expand=True)

    con = scrollablefunc(right,BG)

    main = Frame(con,bg=BG)
    main.pack(fill="x",padx=20,pady=(20,4))
    Label(main, text="Medical History", bg=BG, font=F(20,"bold"),
          fg=TEXT_DARK, anchor="w").pack(side="left")
    
    edit = Label(main,text="Edit",font=FM(10,"bold"),
                 bg=ACCENT,fg="white",padx=12,pady=6,cursor="hand2")
    edit.pack(side="right")

    Label(con, text="Your Medical Information",bg=BG,font=F(13),
          fg=TEXT_MED, anchor="w").pack(fill="x",padx=20)

    Frame(con, height=1, bg=ACCENT).pack(fill="x",pady=10)

    return frame

# from tkinter import *
# from frontend.sidebar import create_sidebar
# from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM

# def historypage(parent, controller):
#     frame = Frame(parent, bg=BG)
# #     user = controller.current_user

#     container = Frame(frame, bg=BG)
#     container.pack(fill="both", expand=True)

#     create_sidebar(container, controller, "Medical History")

#     content = Frame(container, bg=BG)
#     content.pack(side="left", fill="both", expand=True)

#     # ── Header ──────────────────────────────────────────
#     header = Frame(content, bg=BG)
#     header.pack(fill="x", padx=20, pady=(20, 4))

#     Label(header, text="Medical History", bg=BG, font=F(20, "bold"),
#           fg=TEXT_DARK, anchor="w").pack(side="left")

#     edit_btn = Label(header, text="✏ Edit", font=FM(10, "bold"),
#                      bg=ACCENT, fg="white", padx=12, pady=6, cursor="hand2")
#     edit_btn.pack(side="right")

#     Label(content, text="Your medical information", bg=BG, font=F(13),
#           fg=TEXT_MED, anchor="w").pack(fill="x", padx=20)

#     Frame(content, height=1, bg="#DDD8CC").pack(fill="x", pady=10)

#     # ── Form Data ────────────────────────────────────────
#     # Replace these with controller.current_user data from db later
#     fields = {
#         "Blood Type":           "B+",
#         "Height (cm)":          "170",
#         "Weight (kg)":          "65",
#         "Allergies":            "Penicillin, Dust",
#         "Chronic Conditions":   "Type 2 Diabetes, Hypertension",
#         "Past Surgeries":       "Appendectomy (2018)",
#         "Family History":       "Heart Disease, Diabetes",
#         "Lifestyle Notes":      "Non-smoker, occasional alcohol",
#     }

#     form_frame = Frame(content, bg=BG)
#     form_frame.pack(fill="x", padx=32, pady=10)

#     entries = {}   # store Entry widgets
#     labels  = {}   # store display Labels

#     state = {"editing": False}

#     for i, (field, value) in enumerate(fields.items()):
#         # field label
#         Label(form_frame, text=field, font=FM(9), bg=BG,
#               fg=TEXT_MED, anchor="w").grid(row=i*2, column=0, sticky="w", pady=(10, 1))

#         # display label (view mode)
#         lbl = Label(form_frame, text=value, font=FM(11), bg=CARD,
#                     fg=TEXT_DARK, anchor="w", padx=12, pady=8,
#                     highlightthickness=1, highlightbackground="#D8EAE7")
#         lbl.grid(row=i*2+1, column=0, sticky="ew", pady=(0, 2))
#         labels[field] = lbl

#         # entry widget (edit mode) — hidden initially
#         var = StringVar(value=value)
#         ent = Entry(form_frame, textvariable=var, font=FM(11),
#                     bg=PILL_BG, relief="flat", bd=0,
#                     highlightthickness=1, highlightbackground=ACCENT)
#         entries[field] = (ent, var)

#     form_frame.columnconfigure(0, weight=1)

#     # ── Toggle Edit / Save ───────────────────────────────
#     def toggle_edit():
#         if not state["editing"]:
#             # switch to edit mode
#             for field, (ent, var) in entries.items():
#                 labels[field].grid_remove()
#                 ent.grid(row=list(fields.keys()).index(field)*2+1,
#                          column=0, sticky="ew", ipady=7, pady=(0, 2))
#             edit_btn.config(text="💾 Save")
#             state["editing"] = True
#         else:
#             # save and switch back to view mode
#             for field, (ent, var) in entries.items():
#                 new_val = var.get().strip()
#                 labels[field].config(text=new_val)
#                 ent.grid_remove()
#                 labels[field].grid()
#             edit_btn.config(text="✏ Edit")
#             state["editing"] = False

#             save_to_db()

#     edit_btn.bind("<Button-1>", lambda e: toggle_edit())

#     # ── DB Save ──────────────────────────────────────────
#     def save_to_db():
#         data = {field: var.get().strip() for field, (_, var) in entries.items()}
#         # TODO: call your db function here
#         # update_medical_history(user["id"], data)
#         print("Saved:", data)

#     return frame