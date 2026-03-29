import hashlib
from tkinter import *
from tkinter import messagebox
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM
from backend.db import getConnection
from frontend import session 

def loginpage(parent, controller):

      frame = Frame(parent, bg=BG)

      card = Frame(frame, bg=CARD, padx=36, pady=32,
                  relief="flat", bd=0)
      card.place(relx=0.5, rely=0.5, anchor=CENTER)

      # Logo
      logo_canvas = Canvas(card, width=44, height=44, bg=CARD, highlightthickness=0)
      logo_canvas.grid(row=0, column=0, columnspan=2, pady=(0, 4))
      logo_canvas.create_oval(2, 2, 42, 42, fill=ACCENT, outline="")
      logo_canvas.create_text(22, 22, text="✚", font=FM(16, "bold"), fill="white")

      Label(card, text="MediTrack", font=F(15, "bold"),
            bg=CARD, fg=TEXT_DARK).grid(row=1, column=0, columnspan=2)
      Label(card, text="Sign in to your account", font=FM(9),
            bg=CARD, fg=TEXT_LIGHT).grid(row=2, column=0, columnspan=2, pady=(2, 16))

      # Username
      Label(card, text="Username", font=FM(9), bg=CARD,
            anchor="w").grid(row=3, column=0, columnspan=2, sticky="w", padx=2, pady=(6, 1))
      Eusername = Entry(card, width=28, font=FM(10),bg=PILL_BG,bd=0)
      Eusername.grid(row=4, column=0, columnspan=2, ipady=7, padx=2)
      Frame(card, height=2, bg=ACCENT).grid(row=5, column=0, columnspan=2, sticky="ew", padx=2, pady=(0, 4))

      # Password
      Label(card, text="Password", font=FM(9), bg=CARD, 
            anchor="w").grid(row=6, column=0, columnspan=2, sticky="w", padx=2, pady=(6, 1))
      Epassword = Entry(card, width=28, font=FM(10),show="*", bg=PILL_BG, relief="flat", bd=0)
      Epassword.grid(row=7, column=0, columnspan=2, ipady=7, padx=2)
      Frame(card, height=2, bg=ACCENT).grid(row=8, column=0, columnspan=2, sticky="ew", padx=2, pady=(0, 4))

      # Show/Hide toggle
      def toggle_password():
            if Epassword.cget("show") == "":
                  Epassword.config(show="*")
                  toggle_btn.config(text="Show", fg=TEXT_LIGHT)
            else:
                  Epassword.config(show="")
                  toggle_btn.config(text="Hide", fg=ACCENT)

      toggle_btn = Label(card, text="Show", font=FM(8), bg= PILL_BG, fg=TEXT_LIGHT, cursor="hand2")
      toggle_btn.grid(row=7, column=1, sticky="e", padx=6)
      toggle_btn.bind("<Button-1>", lambda e: toggle_password())

      # Login button
      def logindone():
            # check from db, history_filled = true: dashboard or else medical history page
            username = Eusername.get().strip()
            password = Epassword.get().strip()

            if not username or not password:
                  messagebox.showwarning("Input Error","Please enter both the field")
                  return
            
            hashedpass = hashlib.sha256(password.encode()).hexdigest()

            conn = None
            try:
                  conn = getConnection()
                  cursor = conn.cursor(dictionary=True)

                  query = "SELECT * FROM patientinfo WHERE username = %s AND password = %s"
                  cursor.execute(query, (username,hashedpass))
                  patient = cursor.fetchone()

                  if patient:
                        session.patientid = patient['id']
                        print(f"DEBUG: Login successful. ID set to: {session.patientid}")
                        if patient.get('history_filled'):
                              messagebox.showinfo("Success", f"Welcome back, {username}!")
                              controller("dashboard")
                        else:
                              messagebox.showinfo("Success", f"Welcome, {username} to MediTrack!")
                              controller("history")
                  else:
                        messagebox.showwarning("Missing","No user exists")

            except Exception as e:
                  messagebox.showerror("Database Error", f"Error: {e}")
            
            finally:
                  if conn:
                        conn.close()


      def on_enter(e): login_btn.config(bg="#236358")
      def on_leave(e): login_btn.config(bg=ACCENT)

      login_btn = Button(card, text="Sign In", font=FM(10, "bold"),
                        bg=ACCENT, fg="white", bd=0, 
                        activebackground="#236358", activeforeground="white",
                        pady=8, cursor="hand2", command=logindone)
      login_btn.grid(row=9, column=0, columnspan=2, sticky="ew", padx=2, pady=(14, 0))
      login_btn.bind("<Enter>", on_enter)
      login_btn.bind("<Leave>", on_leave)

      # Sign up link
      bottom = Frame(card, bg=CARD)
      bottom.grid(row=10, column=0, columnspan=2, pady=(10, 0))
      Label(bottom, text="Don't have an account?", font=FM(9), bg=CARD, fg=TEXT_MED).pack(side="left")
      signup_link = Label(bottom, text=" Sign Up", font=FM(9, "bold"), bg=CARD, fg=ACCENT, cursor="hand2")
      signup_link.pack(side="left")
      signup_link.bind("<Button-1>", lambda e: controller("signup"))

      return frame
