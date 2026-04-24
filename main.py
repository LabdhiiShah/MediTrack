import threading
from tkinter import *

from frontend.modules import center
from frontend.login import loginpage
from frontend.signup import signuppage
from frontend.dashboard import dashboardpage
from frontend.mymedicine import mymedicinepage
from frontend.reminder import reminderpage
from frontend.history import historypage
from frontend.interaction import interactionpage
from frontend.profile import profilepage
from frontend.food import foodpage

from reminder_service import start_reminder_loop
from tray import build_tray
from autostart import enable_autostart, is_autostart_enabled

def main():
    # 1. Autostart — register silently if not already registered
    if not is_autostart_enabled():
        enable_autostart()

    # 2. Start background reminder thread — called ONCE only
    start_reminder_loop()

    # 3. Build Tkinter window
    root = Tk()
    root.title("MediTrack")
    root.geometry("1100x700")
    center(root, 1100, 700)

    container = Frame(root)
    container.pack(fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    frames = {}

    # sidebar_refreshers: maps page_name → the sidebar's getid function for that page.
    # Each page creates its own sidebar instance; we collect their refresh callbacks
    # here so show() can call getid() every time the user navigates.
    sidebar_refreshers = {}

    def show(page_name):
        frame = frames[page_name]

        # 1. Refresh the page content (load_reminders, load_medicines, etc.)
        if hasattr(frame, "refresh"):
            frame.refresh()

        # 2. Refresh the sidebar for this page — updates the username/avatar
        #    from the current session (important after login / logout)
        if page_name in sidebar_refreshers:
            try:
                sidebar_refreshers[page_name]()
            except Exception as e:
                print(f"[main] sidebar refresh error for {page_name}: {e}")

        frame.tkraise()

    pages = {
        "login"      : loginpage,
        "signup"     : signuppage,
        "dashboard"  : dashboardpage,
        "mymedicine" : mymedicinepage,
        "reminder"   : reminderpage,
        "history"    : historypage,
        "interaction": interactionpage,
        "profile"    : profilepage,
        "diet"       : foodpage
    }

    for name, func in pages.items():
        frame        = func(container, show)
        frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        sidebar = getattr(frame, "sidebar", None)
        if sidebar and hasattr(sidebar, "refresh"):
            sidebar_refreshers[name] = sidebar.refresh

    show("login")

    icon = None

    def show_window():
        root.deiconify()
        root.lift()
        root.focus_force()

    def quit_app():
        if icon:
            icon.stop()
        root.quit()

    icon = build_tray(show_window, quit_app)

    # 5. Hide window on X click instead of closing
    root.protocol("WM_DELETE_WINDOW", root.withdraw)

    # 6. pystray on side thread, tkinter on main thread
    tray_thread = threading.Thread(target=icon.run, daemon=True)
    tray_thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()