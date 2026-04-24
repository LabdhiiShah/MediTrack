import pystray
from PIL import Image

def build_tray(show_window, quit):
    menu = pystray.Menu(
        pystray.MenuItem("Open MediTrack", show_window, default=True),
        pystray.MenuItem("Quit", quit)
    )
    icon = pystray.Icon(
        name  = "MediTrack",
        icon  = Image.open("tray_icon.png"),    
        title = "MediTrack",
        menu  = menu
    )
    return icon