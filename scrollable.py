from tkinter import *

def scrollablefunc(parent, bg):

    main = Frame(parent,bg=bg)
    main.pack(fill="both",expand=True)
    scroll = Canvas(main,bg=bg,highlightthickness=0)
    scrollbar = Scrollbar(main, orient="vertical",command=scroll.yview)
    scroll.configure(yscrollcommand=scrollbar.set)  # moves through mouse
    scrollbar.pack(side="right",fill="y")
    scroll.pack(side="left",fill="both",expand=True)

    content = Frame(scroll,bg=bg)
    content_window = scroll.create_window((0,0),window=content,anchor="nw")

    def on_configure(e):
        scroll.configure(scrollregion=scroll.bbox("all"))
        scroll.itemconfig(content_window, width=scroll.winfo_width()) # content matches canvas size
    content.bind("<Configure>", on_configure)
    scroll.bind("<Configure>", lambda e: scroll.itemconfig(content_window, width=e.width))
    scroll.bind_all("<MouseWheel>", lambda e: scroll.yview_scroll(-1*(e.delta//120),"units"))
    
    return content
