from tkinter import *

def center(window,window_width, window_height ):
	screen_width = window.winfo_screenwidth()
	screen_height = window.winfo_screenheight()

	# Calculate center coordinates
	x = int((screen_width / 2) - (window_width / 2))
	y = int((screen_height / 2) - (window_height / 2))

	# Set geometry with position
	window.geometry(f"{window_width}x{window_height}+{x}+{y}")