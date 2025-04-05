#main copy with keyboard
import pytesseract
import keyboard
from tkinter import Tk, Label
from PIL import ImageGrab
import google.generativeai as genai
from src.autotyper import type_from_clipboard
from src.profile_1 import Profile

# Path to your Tesseract executable (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
GOOGLE_API_KEY="AIzaSyD_JLFtabbujqdLsmSACpdHOHyTBmHL4fQ"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
def setup():
    model.generate_content(Profile)
    model.generate_content(Profile)
    response=model.generate_content("extract interview question from further inputs and give ony response which i can speak directly to the interviewer remove tips and all")
    print(response.text)
def generate(text):
    response = model.generate_content(text)
    return response.text

def capture_text():
    # Capture the entire screen (you can modify this to capture a specific region)
    img = ImageGrab.grab()
    
    # Use OCR to extract text from the captured image
    text = pytesseract.image_to_string(img)
    
    # Return the captured text
    return text.strip()

def generate_answer(text):
    if not text:
        return "No text captured."
    return generate(text)

def show_answer_popup(answer):
    # Create a popup window to display the answer ABOVE all other windows for 10 seconds
    root = Tk()
    root.title("Answer")
    
    # Calculate window size based on answer length
    width = min(400, max(200, len(answer) * 7))
    height = min(1000, max(50, len(answer) // 2))
    
    root.geometry(f"{width}x{height}")
    root.attributes("-topmost", True)  # Ensure the window is above all other windows
    
    label = Label(root, text=answer, wraplength=width - 20)
    label.pack(pady=20)
    # Close the window after 10 secondsWhether job satisfaction should be prioritized over salary when selecting a career is a
    root.mainloop()

def on_shortcut():
    text = capture_text()
    answer = generate_answer(text)
    #copy answer to clipboard
    root = Tk()
    root.clipboard_clear()
    root.clipboard_append(answer)
    root.withdraw()
    root.update()
    root.destroy()
    show_answer_popup(answer)

#main
if __name__ == "__main__":
    setup()
    keyboard.add_hotkey('ctrl+shift+1', on_shortcut)
    print("Press 'Ctrl + Shift + 1' to capture text and get an answer. Press 'Ctrl+Shift+X' to exit.")
    keyboard.add_hotkey('ctrl+shift+h', type_from_clipboard)
    # Keep the script running to listen for the shortcut
    keyboard.wait('Ctrl+Shift+x')  # You can press 'Esc' to exit the program

    print("Press 'Ctrl + Shift + 1' to capture text and get an answer. Press 'Ctrl+Shift+X' to exit.")

    # Keep the script running to listen for the shortcut
    #keyboard.wait('Ctrl+Shift+x')  # You can press 'Esc' to exit the program

    #print("Program exited.")