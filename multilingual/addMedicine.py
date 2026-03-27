from tkinter import *
from config import CARD, ACCENT, TEXT_MED, FM
from i18n import i18n

def add_medicine_popup(add_card):
    popup = Toplevel()
    popup.title(i18n.t("medicines", "popup_title"))
    popup.geometry("300x150")
    popup.resizable(False, False)
    popup.configure(bg=CARD)

    popup.update_idletasks()
    x = (popup.winfo_screenwidth()  - 300) // 2
    y = (popup.winfo_screenheight() - 150) // 2
    popup.geometry(f"300x150+{x}+{y}")

    label = Label(popup, text=i18n.t("medicines", "popup_label"),
                  font=FM(10), bg=CARD, fg=TEXT_MED)
    label.pack(anchor="w", padx=24, pady=(20, 4))

    name_var = StringVar()
    Entry(popup, textvariable=name_var, font=FM(11), width=28,
          bg="#F5F5F5", relief="flat", bd=0,
          highlightthickness=1, highlightbackground="#DDD",
          highlightcolor=ACCENT).pack(ipady=7, padx=24)

    def confirm():
        name = name_var.get().strip()
        if name:
            add_card(name, active=True)
            popup.destroy()

    add_btn = Label(popup, text=i18n.t("medicines", "popup_add"),
                    font=FM(10, "bold"), bg=ACCENT, fg="white",
                    padx=14, pady=7, cursor="hand2")
    add_btn.pack(anchor="e", padx=24, pady=(12, 0))
    add_btn.bind("<Button-1>", lambda e: confirm())
    popup.bind("<Return>", lambda e: confirm())

    # update popup title and labels if language changes while popup is open
    def refresh():
        try:
            popup.title(i18n.t("medicines", "popup_title"))
            label.config(text=i18n.t("medicines", "popup_label"))
            add_btn.config(text=i18n.t("medicines", "popup_add"))
        except Exception:
            pass

    i18n.on_change(refresh)

    return popup
