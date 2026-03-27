
import sounddevice as sd
import numpy as np
import sys

# =============================
# CONFIGURATION
# =============================
SAMPLE_RATE = 16000
BLOCK_SIZE = 1024  # How often we check the volume

def get_volume_bar(volume, threshold=0.02):
    """Creates a visual ASCII bar based on volume."""
    bar_length = 40
    # Scale volume for visualization (0.0 to 0.1 is usually the active range)
    filled_length = int(min(volume * 400, bar_length))
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    
    # Add a marker for the threshold
    status = " [SPEAKING]" if volume > threshold else " [SILENT]  "
    return f"|{bar}| Vol: {volume:.4f} {status}"

def monitor_mic():
    print("--- MediTrack Diagnostic Tool ---")
    print(f"Listing available audio devices:\n{sd.query_devices()}")
    
    # If it's picking the wrong mic, you can change device=None 
    # to the ID number from the list above.
    device_info = sd.query_devices(kind='input')
    print(f"\nUsing Default Input: {device_info['name']}")
    print("Press Ctrl+C to stop.\n")

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        
        # Calculate Root Mean Square (RMS) volume
        volume = np.sqrt(np.mean(indata**2))
        
        # Print the bar and overwrite the line
        sys.stdout.write(f"\r{get_volume_bar(volume)}")
        sys.stdout.flush()

    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, 
                            channels=1, 
                            callback=callback, 
                            blocksize=BLOCK_SIZE):
            while True:
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\n\nDiagnostic stopped.")

if __name__ == "__main__":
    monitor_mic()