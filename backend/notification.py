# # only notification

# from plyer import notification
# import time

# def send_alert(title, message):
#     notification.notify(
#         title=title,
#         message=message,
#         app_name='MediTrack',
#         # app_icon='path/to/icon.ico', # You can add your .ico path here later
#         timeout=10, # How many seconds it stays on screen
#     )

# if __name__ == "__main__":
#     print("Sending immediate notification...")
#     send_alert("MediTrack Test", "This is an instant notification!")

#     print("Waiting 5 seconds for the next one...")
#     time.sleep(5)

#     send_alert("Medicine Reminder", "Time to take your Paracetamol.")
#     print("Done!")




# # Notification with voice 

from plyer import notification
import pyttsx3
import time

def medical_alert(med_name):
    # 1. The Visual (Will show if DND is off)
    notification.notify(
        title="MEDITRACK ALERT",
        message=f"Time to take {med_name}. Please respond.",
        timeout=10
    )
    
    # 2. The Audio (Will ALWAYS play)
    engine = pyttsx3.init()
    engine.setProperty('rate', 150) # Slower speed for seniors
    engine.say(f"Excuse me. It is time to take your medicine, {med_name}.")
    engine.runAndWait()

medical_alert("Aspirin")


# not yet tried 

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import pyttsx3
from plyer import notification
import time
import threading

# --- CONFIGURATION ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "meditrack" # Ensure this matches your XAMPP DB name
}

def update_db_status(med_id, status):
    """Updates the medicine status in MySQL"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "UPDATE reminders SET status = %s WHERE id = %s"
        cursor.execute(query, (status, med_id))
        conn.commit()
        conn.close()
        print(f"Success: Marked ID {med_id} as {status}")
    except Exception as e:
        print(f"DB Update Error: {e}")

def speak_alert(med_name):
    """Voice alert for seniors"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 140) # Slower for clarity
    engine.say(f"Excuse me. It is time to take your medicine: {med_name}. Please check the screen.")
    engine.runAndWait()

def show_interactive_window(med_id, med_name):
    """The Big Button Popup for Seniors"""
    root = tk.Tk()
    root.title("MEDITRACK REMINDER")
    root.attributes('-topmost', True) # Keep on top of all apps
    root.geometry("450x300+500+300") # Centered-ish on screen
    root.configure(bg="#f0f0f0")

    # Heading
    tk.Label(root, text="🔔 MEDICINE TIME", font=("Arial", 20, "bold"), fg="red", bg="#f0f0f0").pack(pady=20)
    
    # Medicine Name
    tk.Label(root, text=f"Please take: {med_name}", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)

    btn_frame = tk.Frame(root, bg="#f0f0f0")
    btn_frame.pack(pady=30)

    def on_taken():
        update_db_status(med_id, "taken")
        root.destroy()

    def on_missed():
        # You can add logic here to notify caretaker immediately or reschedule
        update_db_status(med_id, "missed")
        root.destroy()

    # Big Green "Taken" Button
    tk.Button(btn_frame, text="✅ I HAVE TAKEN IT", font=("Arial", 12, "bold"), 
              bg="#4CAF50", fg="white", width=20, height=2, command=on_taken).grid(row=0, column=0, padx=10)

    # Big Red "Missed" Button
    tk.Button(btn_frame, text="❌ MISS DOSE", font=("Arial", 12, "bold"), 
              bg="#f44336", fg="white", width=15, height=2, command=on_missed).grid(row=0, column=1, padx=10)

    root.mainloop()

def trigger_full_alert(med_id, med_name):
    """Runs Notification, Voice, and Popup together"""
    # 1. System Tray Notification
    notification.notify(
        title="Medicine Reminder",
        message=f"Time for {med_name}",
        timeout=10
    )
    
    # 2. Start Voice in a separate thread so it doesn't block the Window
    threading.Thread(target=speak_alert, args=(med_name,), daemon=True).start()
    
    # 3. Show the interactive buttons
    show_interactive_window(med_id, med_name)

def check_for_reminders():
    """Polls the MySQL database for pending doses"""
    while True:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Select meds where time has passed and they are still 'pending'
            # Note: Ensure your table has 'id', 'brand_name', 'reminder_time', and 'status'
            query = "SELECT id, brand_name FROM reminders WHERE reminder_time <= NOW() AND status = 'pending' LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                print(f"Triggering alert for {result['brand_name']}")
                trigger_full_alert(result['id'], result['brand_name'])
            
            conn.close()
        except Exception as e:
            print(f"Watcher Error: {e}")
            
        time.sleep(30) # Check every 30 seconds

if __name__ == "__main__":
    print("MediTrack Watcher is running in the background...")
    check_for_reminders()