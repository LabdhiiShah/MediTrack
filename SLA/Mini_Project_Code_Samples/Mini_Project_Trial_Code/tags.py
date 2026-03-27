import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_693=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_693["font"] = ft
        GLabel_693["fg"] = "#333333"
        GLabel_693["justify"] = "center"
        GLabel_693["text"] = "User Name"
        GLabel_693.place(x=70,y=140,width=70,height=25)

        GLineEdit_525=tk.Entry(root)
        GLineEdit_525["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_525["font"] = ft
        GLineEdit_525["fg"] = "#333333"
        GLineEdit_525["justify"] = "left"
        GLineEdit_525["text"] = ""
        GLineEdit_525.place(x=210,y=140,width=70,height=25)

        GLabel_140=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_140["font"] = ft
        GLabel_140["fg"] = "#333333"
        GLabel_140["justify"] = "center"
        GLabel_140["text"] = "Password"
        GLabel_140.place(x=70,y=210,width=70,height=25)

        GLineEdit_228=tk.Entry(root)
        GLineEdit_228["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_228["font"] = ft
        GLineEdit_228["fg"] = "#333333"
        GLineEdit_228["justify"] = "left"
        GLineEdit_228["text"] = ""
        GLineEdit_228.place(x=210,y=220,width=70,height=25)

        GButton_165=tk.Button(root)
        GButton_165["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_165["font"] = ft
        GButton_165["fg"] = "#000000"
        GButton_165["justify"] = "center"
        GButton_165["text"] = "submit"
        GButton_165.place(x=80,y=320,width=70,height=25)
        GButton_165["command"] = self.GButton_165_command

        GButton_71=tk.Button(root)
        GButton_71["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_71["font"] = ft
        GButton_71["fg"] = "#000000"
        GButton_71["justify"] = "center"
        GButton_71["text"] = "Reset"
        GButton_71.place(x=210,y=320,width=70,height=25)
        GButton_71["command"] = self.GButton_71_command

    def GButton_165_command(self):
        print("command")


    def GButton_71_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
