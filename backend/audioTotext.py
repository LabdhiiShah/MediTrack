# import sounddevice as sd
# import numpy as np
# from faster_whisper import WhisperModel
# import collections

# # =============================
# # CONFIGURATION
# # =============================
# MODEL_SIZE = "small"    # "base" for speed, "small" for better Marathi/Gujarati
# DEVICE = "cpu"          # Use "cuda" if you have an NVIDIA GPU
# COMPUTE_TYPE = "int8"   # Optimized for CPU

# # Audio Settings
# SAMPLE_RATE = 16000
# SILENCE_THRESHOLD = 0.01  # ADJUST THIS: Increase if it hears "ghosts", decrease if it misses your voice
# CHUNK_SIZE = 1024         # Small chunks for processing
# MAX_BUFFER_SECONDS = 3    # How many seconds to listen before translating

# print(f"--- Loading {MODEL_SIZE} model on {DEVICE} ---")
# model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
# print("Model Ready. Speak now (Ctrl+C to exit).\n")

# def run_translator():
#     # A deque automatically manages our memory buffer
#     audio_buffer = collections.deque(maxlen=int(SAMPLE_RATE * MAX_BUFFER_SECONDS / CHUNK_SIZE))
    
#     def callback(indata, frames, time, status):
#         # Calculate the volume level (RMS)
#         volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))
        
#         # Only add to buffer if there is actual sound
#         if volume_norm > SILENCE_THRESHOLD:
#             audio_buffer.append(indata.copy())
#         elif len(audio_buffer) > 0:
#             # If we were recording but it's now silent, add a tiny bit of padding
#             # This helps the model "finish" the last word properly
#             audio_buffer.append(np.zeros_like(indata))

#     try:
#         with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=CHUNK_SIZE):
#             while True:
#                 # Process when buffer is roughly full (e.g., every 2-3 seconds)
#                 if len(audio_buffer) >= (audio_buffer.maxlen * 0.7):
#                     # Combine chunks into one audio array
#                     combined_audio = np.concatenate(list(audio_buffer)).flatten()
#                     audio_buffer.clear()

#                     # Transcribe with strict settings
#                     segments, info = model.transcribe(
#                         combined_audio,
#                         task="translate",    # Forces English output
#                         vad_filter=True,     # Second layer of silence removal
#                         vad_parameters=dict(min_silence_duration_ms=500),
#                         beam_size=5,         # Better quality for Indian languages
#                         no_speech_threshold=0.6, # If 60% sure it's noise, ignore it
#                         condition_on_previous_text=False # Prevents repeating lines
#                     )

#                     for segment in segments:
#                         if segment.text.strip():
#                             # Show which language it detected (e.g., mr, gu, en)
#                             print(f"[{info.language}] >> {segment.text.strip()}")

#     except KeyboardInterrupt:
#         print("\nStopping... Goodbye!")

# if __name__ == "__main__":
#     run_translator()

# ------------------------------------------------------------------------------------------------------------------------------------------
# my final was:

import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import queue

# =============================
# CONFIGURATION
# =============================
MODEL_SIZE = "small"
DEVICE = "cpu"
COMPUTE_TYPE = "int8"

SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.02  # Adjust if it's too sensitive
SILENCE_DURATION = 1.0    # Seconds of silence to trigger translation

# Filters
ALLOWED_LANGS = ['en', 'mr', 'gu', 'hi']
BANNED = ["subscribe", "watching", "video", "channel", "thanks for"]

print(f"--- MediTrack V2: Waiting for complete sentences ---")
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

audio_queue = queue.Queue()

def callback(indata, frames, time, status):
    audio_queue.put(indata.copy())

def run_translator():
    full_audio = []
    silent_chunks = 0
    
    # Calculate how many chunks make up 1 second
    chunks_per_second = SAMPLE_RATE / 1024 

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=1024):
        print("Ready. Speak a full sentence and then pause...")
        
        while True:
            chunk = audio_queue.get()
            volume = np.linalg.norm(chunk) / np.sqrt(len(chunk))
            
            if volume > SILENCE_THRESHOLD:
                full_audio.append(chunk)
                silent_chunks = 0 # Reset silence counter
            else:
                silent_chunks += 1
                if len(full_audio) > 0: # If we have recorded speech
                    full_audio.append(chunk) # Keep a bit of silence for context
                
            # If we have speech in the buffer AND we've been silent for 1 second
            if len(full_audio) > (SAMPLE_RATE/2) and silent_chunks > chunks_per_second:
                audio_data = np.concatenate(full_audio).flatten()
                full_audio = [] # Clear buffer
                silent_chunks = 0

                segments, info = model.transcribe(
                    audio_data,
                    task="translate",
                    beam_size=5,
                    vad_filter=True,
                    initial_prompt="A medical consultation in English, Marathi, or Gujarati."
                )

                if info.language in ALLOWED_LANGS:
                    for segment in segments:
                        text = segment.text.strip()
                        if text and not any(p in text.lower() for p in BANNED):
                            print(f"[{info.language}] >> {text}")

if __name__ == "__main__":
    try:
        run_translator()
    except KeyboardInterrupt:
        print("\nStopping MediTrack...")