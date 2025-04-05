import pyaudio
import speech_recognition as sr
import keyboard
import threading
import wave

# Create a recognizer object
r = sr.Recognizer()

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
                    rate=44100,
                    input=True,
                    input_device_index=input_device_index,
                    frames_per_buffer=1024)

    print("Listening to system audio...")

    while True:
        # Read audio data from the stream
        data = stream.read(1024)
        audio = sr.AudioData(data, 44100, 2)

        try:
            # Use the recognizer to convert speech to text using Windows Speech Recognition
            text = r.recognize_windows(audio)
            print("You said:", text)
        except sr.UnknownValueError:
            print("Windows Speech Recognition could not understand audio")
            # Save the audio data for debugging
            with wave.open("unrecognized_audio.wav", "wb") as f:
                f.setnchannels(1)
                f.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                f.setframerate(44100)
                f.writeframes(data)
        except sr.RequestError as e:
            print(f"Could not request results from Windows Speech Recognition service; {e}")

# Function to start listening
def start_listening():
    listener_thread = threading.Thread(target=listen_system_audio)
    listener_thread.start()

# Register hotkey to start/stop listening
keyboard.add_hotkey('ctrl+shift+l', start_listening)
print("Press 'Ctrl + Shift + L' to start listening. Press 'Esc' to exit.")

# Keep the script running to listen for the hotkey
keyboard.wait('esc')
print("Exited.")