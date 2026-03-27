import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import queue
import sys

# =============================
# CONFIGURATION
# =============================
MODEL_SIZE = "small" # "medium" is MUCH better for Marathi/Gujarati translation if your PC can handle it
DEVICE = "cpu"
COMPUTE_TYPE = "int8"

SAMPLE_RATE = 16000
BLOCK_SIZE = 1024
SILENCE_THRESHOLD = 0.01 
SILENCE_DURATION = 1.5   

print(f"--- MediTrack V2: Forced Translation Mode ---")
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
audio_queue = queue.Queue()

def callback(indata, frames, time, status):
    audio_queue.put(indata.copy())

def run_translator():
    buffer = []
    silent_chunks = 0
    chunks_per_sec = SAMPLE_RATE / BLOCK_SIZE 

    print("\n[DEBUG MODE] Listening...")
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=BLOCK_SIZE):
        while True:
            chunk = audio_queue.get()
            volume = np.linalg.norm(chunk) / np.sqrt(len(chunk))
            
            if volume > SILENCE_THRESHOLD:
                buffer.append(chunk)
                silent_chunks = 0
            else:
                silent_chunks += 1
                
            if len(buffer) > 0 and silent_chunks > (SILENCE_DURATION * chunks_per_sec):
                print(f"DEBUG: Processing {len(buffer)} chunks...")
                
                audio_data = np.concatenate(buffer).flatten().astype(np.float32)
                
                # We remove almost all constraints to see what's happening
                segments, info = model.transcribe(
                    audio_data,
                    task="translate",
                    beam_size=1,        # Faster processing
                    vad_filter=False    # Turn off VAD to see if it's cutting you off
                )

                print(f"DEBUG: Detected Language: {info.language} (Prob: {info.language_probability:.2f})")

                for segment in segments:
                    # Raw print - no filters
                    print(f"RAW TEXT: '{segment.text}' | Confidence: {1 - segment.no_speech_prob:.2f}")

                buffer = []
                silent_chunks = 0
                print("-" * 30)
                
if __name__ == "__main__":
    try:
        run_translator()
    except KeyboardInterrupt:
        print("\nStopping...")