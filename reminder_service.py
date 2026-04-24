import time
import threading
import pyttsx3  # text to speech
from datetime import datetime, date, timedelta
from plyer import notification  # sends notification
from frontend import session
from backend.db import getConnection

# stores notifications which are fired at runtime, so no duplicate notification for missed medicines or current reminders
# stores: (reminder_id, date, time)
_notified_this_session: set = set()

# used as a flag for queries or task to complete after every 24 hours
_midnight_logged_date: date | None = None

# converts string to date time object
def _parse_time(t: str) -> datetime | None:
    for time in ("%I:%M %p", "%I:%M%p", "%-I:%M %p"):
        try:
            return datetime.strptime(t.strip(), time)
        except (ValueError, TypeError):
            pass
    return None

# matches current time
def _times_match(db_timing: str, now: datetime) -> bool:
    parsed = _parse_time(db_timing)
    if parsed is None:
        return False
    # as parsed in date time object can access hour and minute
    return parsed.hour == now.hour and parsed.minute == now.minute

def medical_alert(medicine_name, tablets):
    notification.notify(
        title   = "MediTrack 💊",
        message = f"Time for {medicine_name} — {tablets} tablet(s)",
        app_name= "MediTrack",
        timeout = 10
    )
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(f"Excuse me. It is time to take your medicine, {medicine_name}.")
    engine.runAndWait()

def missed_medical_alert(medicine_name, tablets):
    notification.notify(
        title   = "MediTrack 💊",
        message = f"Reminder for {medicine_name} — {tablets} tablet(s), you missed",
        app_name= "MediTrack",
        timeout = 10
    )
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(f"Excuse me. You missed to take your medicine, {medicine_name}.")
    engine.runAndWait()

# checks if there's any schedule today
def _is_scheduled_today(row, today: date) -> bool:
    start     = row['start_date']
    end       = row['end_date']
    frequency = row.get('frequency', 1) or 1
    if not (start <= today <= end):
        return False
    return (today - start).days % frequency == 0

# all the active reminders
def _get_active_reminders(cursor, today: date):
    cursor.execute("""
        SELECT * FROM reminders WHERE  is_done = 0
          AND  start_date <= %s AND  end_date   >= %s AND  patient_id = %s
        """, (today, today, session.patientid))
    return cursor.fetchall()

# if the entry for reminder is already lofgged
def _already_logged(cursor, reminder_id, today: date) -> bool:
    cursor.execute("""
        SELECT 1 FROM reminder_logs
        WHERE  reminder_id = %s AND logged_date = %s
    """, (reminder_id, today))
    return cursor.fetchone() is not None

# Notifies user of any doses whose scheduled time has already passed today and haven't been logged yet. 
def check_missed_on_startup():

    now   = datetime.now()
    today = now.date()

    conn = None
    try:
        conn = getConnection()
        cur  = conn.cursor(dictionary=True)
        rows = _get_active_reminders(cur, today)

        for row in rows:
            if not _is_scheduled_today(row, today):
                continue

            session_key = (row['reminder_id'], str(today), 'startup')
            if session_key in _notified_this_session:
                continue
            if _already_logged(cur, row['reminder_id'], today):
                _notified_this_session.add(session_key)
                continue

            reminder_dt = _parse_time(row['timing'])
            if reminder_dt is None:
                continue

            if (reminder_dt.hour, reminder_dt.minute) < (now.hour, now.minute):
                missed_medical_alert(row['medicine_name'],row['timing'])
                _notified_this_session.add(session_key)

    except Exception as e:
        print(f"[reminder_service] startup check error: {e}")
    finally:
        if conn: conn.close()

# medicines with missed dose are added in reminder_logs with status = 'missed'
def auto_log_missed_at_midnight():
    global _midnight_logged_date
    today = date.today()

    if _midnight_logged_date == today:
        return

    conn = None
    try:
        conn = getConnection()
        cur  = conn.cursor(dictionary=True)

        cur.execute(
            "SELECT * FROM reminders WHERE is_done = 0 AND patient_id = %s",
            (session.patientid,)
        )
        rows = cur.fetchall()

        for row in rows:
            if not _is_scheduled_today(row, today):
                continue
            if _already_logged(cur, row['reminder_id'], today):
                continue

            cur.execute("""
                INSERT IGNORE INTO reminder_logs
                    (reminder_id, patient_id, status, logged_date, logged_time)
                VALUES (%s, %s, 'missed', %s, '23:59:00')
            """, (row['reminder_id'], row['patient_id'], today))
            print(f"[midnight] Logged missed for reminder_id={row['reminder_id']} on {today}")

        conn.commit()
        _midnight_logged_date = today

    except Exception as e:
        print(f"Error in Reminder service: {e}")
    finally:
        if conn: conn.close()

def check_and_notify():
    now   = datetime.now()
    today = now.date()
    conn  = None
    try:
        conn = getConnection()
        cur  = conn.cursor(dictionary=True)
        rows = _get_active_reminders(cur, today)

        for row in rows:
            if not _is_scheduled_today(row, today):
                continue
            if not _times_match(row['timing'], now):
                continue

            session_key = (row['reminder_id'], str(today), f"{now.hour}:{now.minute}")
            if session_key in _notified_this_session:
                continue

            cur.execute("""
                SELECT 1 FROM reminder_logs
                WHERE  reminder_id = %s AND logged_date = %s AND status = 'taken'
            """, (row['reminder_id'], today))
            if cur.fetchone():
                _notified_this_session.add(session_key)
                continue

            medical_alert(row['medicine_name'], row['tablets'])
            _notified_this_session.add(session_key)

        # Midnight trigger
        if now.hour == 23 and now.minute >= 55:
            auto_log_missed_at_midnight()

    except Exception as e:
        print(f"[reminder_service] notify error: {e}")
    finally:
        if conn: conn.close()

def start_reminder_loop():
    def loop():
        print("Reminder service thread starts in background")
        # waits for user to login 
        while not session.patientid:
            time.sleep(2)

        check_missed_on_startup()
        while True:
            if session.patientid:
                check_and_notify()
            time.sleep(60)

    t      = threading.Thread(target=loop, daemon=True)
    t.name = "ReminderThread"
    t.start()