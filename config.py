from tkinter import font as tkfont

BG          = "#F5F0E8"          # warm parchment
CARD        = "#FFFFFF"
ACCENT      = "#2D7D6F"          # teal-green (medical + calm)
ACCENT2     = "#E8834A"          # warm orange for alerts/highlights
TEXT_DARK   = "#1A2B2A"
TEXT_MED    = "#4A6560"
TEXT_LIGHT  = "#8FA8A3"
PILL_BG     = "#E6F4F1"
DANGER      = "#C0392B"
WARN        = "#E67E22"
SAFE        = "#27AE60"
ACCENT_DK   = "#1D6B52"  
SURFACE     = "#F4F4F4"  
BORDER      = "#E0E0E0"  
SECTION_BG  = "#F0F7F5"

def F(size, weight="normal", slant="roman"):
    return tkfont.Font(family="Georgia", size=size, weight=weight, slant=slant)

def FM(size, weight="normal"):
    return tkfont.Font(family="Helvetica", size=size, weight=weight)
