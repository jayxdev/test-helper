import os
import vosk
import json
import pyaudio
import tkinter as tk
from threading import Thread
import csv
from fuzzywuzzy import process
import requests

# Load QA data from CSV
def load_qa_data(csv_path):
    qa_data = {}
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                question = row['Question'].strip().lower()  # Normalize to lower case
                answer = row['Answer'].strip()
                qa_data[question] = answer
    return qa_data

# Initialize QA data
qa_data = load_qa_data("qa.csv")  # Update with your CSV file path

# Function to fetch answers based on CSV data
def get_answer(question):
    question_lower = question.strip().lower()  # Normalize to lower case
    print(f"Looking up question: {question_lower}")  # Debugging statement
    
    # Fuzzy matching to find the closest question
    closest_match, score = process.extractOne(question_lower, qa_data.keys())
    
    if score > 80:  # You can adjust the threshold as needed
        return qa_data[closest_match]
    else:
        return "Sorry, I don't have an answer for that question."

# Function to simulate fetching answer from Gemini with context and QA details
conversation_history = []  # List to store question-answer context


# Function to simulate fetching answer from Gemini with context and QA details
def get_answer_from_gemini(question):
    global conversation_history
    # Check if the question matches CSV-related content first
    answer = get_answer(question)
    if answer and answer != "Sorry, I don't have an answer for that question.":
        return answer

    # Include the previous conversation as context for Gemini
    context = "\n".join([f"Q: {q['question']}\nA: {q['answer']}" for q in conversation_history])
    
    # Replace with your Gemini API URL and key
    gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"  
    headers = {"Authorization": "Bearer YOUR_GEMINI_API_KEY"}  # Replace with your actual API key
    data = {
        "question": question,
        "context": context
    }
    
    try:
        response = requests.post(gemini_api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        answer = result.get('answer', "Sorry, I don't have an answer for that question.")
    except requests.RequestException as e:
        print(f"Gemini API call failed: {e}")
        answer = "Sorry, I don't have an answer for that question."
    
    return answer


# Function to update the answer on the Tkinter window and manage context
def update_answer_label(question_text):
    answer = get_answer_from_gemini(question_text)
    
    # Update GUI with the generated answer
    answer_label.config(text=answer)
    
    # Store the question and answer in conversation history
    conversation_history.append({"question": question_text, "answer": answer})

# Function to handle speech recognition using Vosk
def recognize_speech():
    vosk.SetLogLevel(0)
    model = vosk.Model("./src/vosk-model-small-en-us-0.15")  # Path to your Vosk model
    recognizer = vosk.KaldiRecognizer(model, 16000)

    # Initialize PyAudio for microphone input
    p = pyaudio.PyAudio()
    input_device_index = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if "Stereo Mix" in dev['name'] or "Loopback" in dev['name']:
            input_device_index = i
            break
    if input_device_index is None:
        print("Stereo Mix or Loopback device not found.")
        return
    
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,  # Match recognizer's sample rate
                        input=True,
                        input_device_index=input_device_index,
                        frames_per_buffer=8192)
        print("Listening to system audio...")
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if not data:
                print("No audio data received.")
                continue
            
            # Debugging: Check the size of the data
            print(f"Received data size: {len(data)}")

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                print(f"Raw recognition result: {result}")  # Debugging statement
                result_dict = json.loads(result)
                question_text = result_dict.get('text', '')
                if question_text:
                    print("Recognized question:", question_text)
                    # Update answer label on the GUI and keep track of context
                    update_answer_label(question_text)
            else:
                partial_result = recognizer.PartialResult()
                partial_result_dict = json.loads(partial_result)
                question_label.config(text=f'Question: {partial_result_dict.get("partial", "")}')
                print(f"Partial recognition result: {partial_result}")  # Debugging partial results
            
    except OSError as e:
        print(f"Failed to open stream: {e}")
    finally:
        # Ensure proper cleanup
        stream.stop_stream()
        stream.close()
        p.terminate()

# Tkinter GUI Setup
root = tk.Tk()
screen_width = root.winfo_screenwidth()
root.geometry(f"{screen_width}x100+0+0")
root.configure(bg='black')
root.attributes('-alpha', 0.8)
root.attributes("-topmost", True)
root.title("Interview Helper")

# Label to display the recognized question
question_label = tk.Label(root, text="Recognized Question:", font=("Arial", 14),fg="white", bg="black")
question_label.pack(pady=10)

# Label to display the generated answer
answer_label = tk.Label(root, text="Answer will appear here", font=("Arial", 14),fg="white", bg="black", wraplength=500)
answer_label.pack(pady=10)
# Function to adjust the height of the window based on the content
def adjust_height(event=None):
    root.update_idletasks()
    new_height = answer_label.winfo_reqheight() + question_label.winfo_reqheight() + 40  # Add some padding
    root.geometry(f"{screen_width}x{new_height}+0+0")

# Bind the adjust_height function to the <Configure> event of the answer_label
answer_label.bind("<Configure>", adjust_height)

# Start speech recognition in a separate thread to avoid blocking the Tkinter mainloop
speech_thread = Thread(target=recognize_speech)
speech_thread.daemon = True
speech_thread.start()

# Start the Tkinter event loop
root.mainloop()
