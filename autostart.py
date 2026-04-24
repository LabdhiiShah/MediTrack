"""
imports beacuse we are using system-level informations and windows registry access
firstly, it checks if our app already exists in the starup registry, registered
if not exists then add it
"""
import os
import sys
import winreg

APP_NAME = "MediTrack"

"""
REG_SZ	    => String (text)
REG_DWORD   => Integer (32-bit number)
REG_QWORD   => Large integer (64-bit)
REG_BINARY  => Raw bytes
"""
def enable_autostart():
    """Register MediTrack to launch on Windows boot."""
    exe_path = sys.executable          # full path to python.exe
    script   = os.path.abspath(__file__)          # full abstract path to main.py, __file__ contains the path used to load current script  
    command  = f'"{exe_path}" "{script}"'         # combines this, as windows requires this, it can only understand & run executable files

    try:    
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE 
        )
        # winreg.SetValueEx(key, value_name, reserved, value_type, value_data)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)    
        print("autostart enabled")
        return True
    except Exception as e:
        print("autostart Failed to enable: {e}")
        return False
    

def disable_autostart():
    """Remove MediTrack from Windows startup registry. not used anywhere but if required"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        print("[autostart] Disabled.")
        return True
    except FileNotFoundError:
        print("[autostart] Was not registered, nothing to remove.")
        return True
    except Exception as e:
        print(f"[autostart] Failed to disable: {e}")
        return False

"""
OpenKey(key, sub_key, reserved, access)

tells window which registry root to choose,
winreg.
HKEY_LOCAL_MACHINE -> all users are present
HKEY_CURRENT_USER -> current users

r"Software\Microsoft\Windows\CurrentVersion\Run"  => exact startup location inside registry
The r means raw string (so backslashes are not escaped)
0 => called as "reserved" not used anymore, exists because windows API expects it
"""
def is_autostart_enabled():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_READ
        )

        # checks if the app exists, if not raises error
        winreg.QueryValueEx(key, APP_NAME)

        # Closes the opened registry handle
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False