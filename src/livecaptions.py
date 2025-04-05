import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer
import tkinter as tk
import threading

# Set up Vosk Model (Ensure you download the offline model)
model = Model("./src/vosk-model-small-en-us-0.15")  # Adjust the path to your Vosk model

# Function to update captions safely from any thread
def update_caption_safe(text):
    # Use Tkinter's after method to schedule the update in the main thread
    captions.after(0, update_caption, text)

def update_caption(text):
    captions.config(text=text)
    root.update()

# Get the index of the stereo mix audio input device
# Function to listen to the system audio
def listen_system_audio():
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Find the system's stereo mix or loopback device
    input_device_index = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if "Stereo Mix" in dev['name'] or "Loopback" in dev['name']:
            input_device_index = i
            break
    if input_device_index is None:
        print("Stereo Mix or Loopback device not found.")
        return

    # Open the stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=96000,
                    input=True,
                    input_device_index=input_device_index,
                    frames_per_buffer=1024)

    print("Listening to system audio...")
    rec = KaldiRecognizer(model, 96000)
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result_dict = json.loads(result)
            update_caption_safe(result_dict.get('text', ''))
        else:
            partial_result = rec.PartialResult()
            result_dict = json.loads(partial_result)
            update_caption_safe(result_dict.get('partial', ''))
        

# Function to start listening
def start_listening():
    listener_thread = threading.Thread(target=listen_system_audio)
    listener_thread.daemon = True
    listener_thread.start()

# Tkinter GUI for displaying captions
root = tk.Tk()
root.title("Offline Live Captions")
root.geometry("800x300")
captions = tk.Label(root, text="Captions will appear here...", font=("Helvetica", 24), wraplength=700)
captions.pack(pady=20)

# Start listening to system audio when the GUI starts
start_listening()

# Run the Tkinter event loop
root.mainloop()
