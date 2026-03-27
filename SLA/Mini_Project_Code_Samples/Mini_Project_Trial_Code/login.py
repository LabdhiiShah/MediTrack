from tkinter import *
import mysql.connector  
def submitact():     
    user = Username.get()
    passw = password.get()
    #print(f"The name entered by you is {user} {passw}")
    logintodb(user, passw)   
def logintodb(user, passw):
    con = mysql.connector.connect(
              host="localhost",
              user="root",
              password="",
              database="company"
              )
    cursor = con.cursor()         
    # A Table in the database
    savequery = "select * from login"     
    try:
        cursor.execute(savequery)
        myresult = cursor.fetchall()
        status=False 
        # Printing the result of the
        # query
        for x in myresult:
            if x[0]==user and x[1]==passw :
                status=True
                break;
        if status:    
            w1=Tk()
            f1=Frame(master=w1)
            f1.pack()
            lbl1 = Label(master=f1, text="Login Successful")
            lbl1.pack()

            print("Login Sccessful")
        else:
            w2=Tk()
            f2=Frame(master=w2)
            f2.pack()
            lbl2 = Label(master=f2, text="Login Unsuccessful")
            lbl2.pack()
            print("Login Failed") 
    except:
        db.rollback()
        print("Error occured") 
# Creating GUI 
root = Tk()
root.geometry("300x300")
root.title("Login Page")
# Definging the first row
lblfrstrow = Label(root, text ="Username -", )
lblfrstrow.place(x = 50, y = 20)
Username = Entry(root, width = 35)
Username.place(x = 150, y = 20, width = 100)
lblsecrow = Label(root, text ="Password -")
lblsecrow.place(x = 50, y = 50)
password = Entry(root, show="*",width = 35)
password.place(x = 150, y = 50, width = 100) 
submitbtn = Button(root, text ="Login",
                      bg ='blue', command = submitact)
submitbtn.place(x = 150, y = 135, width = 55) 
root.mainloop()