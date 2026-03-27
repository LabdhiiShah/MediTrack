from tkinter import *
from tkinter import font as tkfont
from tkcalendar import DateEntry
from tkinter import filedialog
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, ACCENT2, TEXT_DARK, TEXT_MED, TEXT_LIGHT, PILL_BG, F, FM

def signuppage(parent, controller):
    frame = Frame(parent,bg=BG)

    # ── Scrollable card area ─────────────────────────────────────────────────
    card = Frame(frame, bg=CARD, padx=36, pady=32,
                 highlightbackground="#D8EAE7", highlightthickness=0)
    card.place(relx=0.5, rely=0.5, anchor=CENTER)

    card.columnconfigure(0, weight=1, pad=10)
    card.columnconfigure(1, weight=1, pad=10)

    # ── Logo + header ────────────────────────────────────────────────────────
    logo_c = Canvas(card, width=44, height=44, bg=CARD, highlightthickness=0)
    logo_c.grid(row=0, column=0, columnspan=2, pady=(0, 4))
    logo_c.create_oval(2, 2, 42, 42, fill=ACCENT, outline="")
    logo_c.create_text(22, 22, text="✚", font=FM(17, "bold"), fill="white")

    Label(card, text="Create Account", font=F(16, "bold"),
          bg=CARD, fg=TEXT_DARK).grid(row=1, column=0, columnspan=2)
    Label(card, text="Join MediTrack today", font=FM(10),
          bg=CARD, fg=TEXT_LIGHT).grid(row=2, column=0, columnspan=2, pady=(2, 16))

    mail = Label(card,text="E-mail id:",font=FM(9),bg=CARD,anchor="w")
    mail.grid(row=3,column=0,sticky="w")

    Email = Entry(card,width=28,font=FM(10),bg=PILL_BG,bd=0,relief="flat")
    Email.grid(row=4, column=0, ipady=7, padx=2,sticky="ew")
    Frame(card,bg=ACCENT,height=2).grid(row=5,column=0,padx=2,sticky="ew")

    # username -> ~cache
    username = Label(card,text="Username:",font=FM(10),bg=CARD,anchor="w")
    username.grid(row=3,column=1,padx=2,sticky="w")

    Eusername = Entry(card,width=28,font=FM(10),bg=PILL_BG,bd=0,relief="flat")
    Eusername.grid(row=4,column=1,padx=2,ipady=7,sticky="ew")
    Frame(card, height=2, bg=ACCENT).grid(row=5, column=1,padx=2,sticky="ew")

    # password -> ~strong password? eye btn(toogle),
    password = Label(card,text="Password:",font=FM(10),bg=CARD)
    password.grid(row=6,column=0,sticky="w")

    Epassword = Entry(card,width=28, show="*",font=FM(11),bg=PILL_BG,bd=0,relief="flat")
    Epassword.grid(row=7,column=0,padx=2,ipady=7,sticky="ew")
    Frame(card, height=2, bg=ACCENT).grid(row=8, column=0, padx=2,sticky="ew")

    def toggle_pass():
        if Epassword.cget("show") == "":
            Epassword.config(show="*")
            t1.config(text="Show", fg=TEXT_LIGHT)
        else:
            Epassword.config(show="")
            t1.config(text="Hide", fg=ACCENT)

    t1 = Label(card, text="Show", font=FM(8), bg=PILL_BG, fg=TEXT_LIGHT, cursor="hand2")
    t1.grid(row=7, column=0, sticky="e", padx=6)
    t1.bind("<Button-1>", lambda e: toggle_pass())

    # confirm password -> ~eye btn(toogle)
    Cpassword = Label(card,text="Confirm Password:",font=FM(10),bg=CARD)
    Cpassword.grid(row=6,column=1,padx=2,sticky="w")

    CEpassword = Entry(card,width=28, show="*",font=FM(11),bg=PILL_BG,bd=0,relief="flat")
    CEpassword.grid(row=7,column=1,padx=2,ipady=7,sticky="ew")
    Frame(card, height=2, bg=ACCENT).grid(row=8, column=1, padx=2,sticky="ew")

    # contact -> ~validation (10 digits)
    contact = Label(card,text="Contact:",font=FM(10),bg=CARD)
    contact.grid(row=9,column=0,padx=2,sticky="w")

    Econtact = Entry(card,width=25,font=FM(11),bg=PILL_BG,bd=0,relief="flat")
    Econtact.grid(row=10,column=0,padx=2,ipady=7,sticky="ew")
    Frame(card, height=2, bg=ACCENT).grid(row=11, column=0, padx=2,sticky="ew")

    # DOB -> ~in db, age column 
    Ldob = Label(card,text="DOB:",font=FM(10),bg=CARD)
    Ldob.grid(row=9,column=1,padx=2,sticky="w")

    dobentry = DateEntry(card,width=25,year=1950,font=FM(11))
    dobentry.grid(row=10,column=1,padx=2,pady=6,sticky="ew")


    # disclaimer -> link to another frame, where something is writen, if checked then only continue
    disclaimerstate = IntVar()
    dis_row = Frame(card, bg=CARD)
    dis_row.grid(row=12, column=0, pady=6, sticky="ew")

    Checkbutton(dis_row, variable=disclaimerstate, bg=CARD,
                activebackground=CARD, selectcolor=PILL_BG).pack(side="left")
    Label(dis_row, text="I agree to the ", font=FM(10),
        bg=CARD, fg=TEXT_MED).pack(side="left")
    dis_link = Label(dis_row, text="Disclaimer", font=FM(10, "bold"),
                    bg=CARD, fg=ACCENT2, cursor="hand2")
    dis_link.pack(side="left")
    dis_link.bind("<Button-1>", lambda e: controller("disclaimer"))

    # profile pic -> save, show

    def upload_pic():
        file = filedialog.askopenfilename(
            filetypes=[("Image Files","*.png *.jpg *.jpeg")]
        )
        print(file)
    picbtn = Button(card,text="Upload Profile Picture",command=upload_pic,font=FM(11))
    picbtn.grid(row=12,column=1,padx=2,pady=6,sticky="ew")

    def on_enter(e): signupbtn.config(bg="#236358")
    def on_leave(e): signupbtn.config(bg=ACCENT)

    # signup button -> successful? -> login
    signupbtn = Button(card,text="Sign Up",font=FM(11,"bold"),
                       bg=ACCENT,fg="white",bd=0,
                       activebackground="#236358",activeforeground="white",
                       pady=8,cursor="hand2",
                       command=lambda: controller("login"))
    signupbtn.grid(row=13, column=0, columnspan=2, padx=2, pady=(14, 0), sticky="ew")

    signupbtn.bind("<Enter>", on_enter)
    signupbtn.bind("<Leave>", on_leave)

    # login option

    bottom = Frame(card,bg=BG)
    bottom.grid(row=14, column=0, columnspan=2, pady=(10, 0))
    Label(bottom,text="Already have an account?",font=FM(10),
            bg=CARD).pack(side="left")

    login_link = Label(bottom, text = "Login", font=FM(10,"bold"),bg=CARD,fg=ACCENT,cursor="hand2")
    login_link.pack(side="left")
    login_link.bind("<Button-1>", lambda e: controller("login"))
    

    return frame