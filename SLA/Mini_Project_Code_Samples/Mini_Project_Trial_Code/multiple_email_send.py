#Reference - https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/
import smtplib
#list of recipients
receivers=['mrsolanki1903@gmail.com','manish.solanki@sbmp.ac.in']
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
sender="mrsolanki1903@gmail.com"
#receiver="manish_ratilal2002@yahoo.com"
password="16 char code"
# Authentication
s.login(sender, password)
for receiver in receivers:
    # message to be sent
    message = "This is a test email from Python Code"
    # sending the mail
    s.sendmail(sender, receiver, message)
    print("Email sent Successfully!!!")
# terminating the session
s.quit()