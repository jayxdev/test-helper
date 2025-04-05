#English mcq and speaking text reader


#main copy with keyboard
import keyboard
import tkinter as tk
from PIL import ImageGrab
from src import gemini
import src.ocr as ocr

# Path to your Tesseract executable (adjust if needed)
model=gemini.setup()
def setup():
    response = gemini.generate(model,"Extract multiple-choice question (MCQs) from the provided text and return only the correct answer for MCQ, or give speaking ans foe 50seconds ")
    if not response:
        print("Failed to setup the model.")
    else:
        print("Model setup complete.")

def generate_answer(text):
    if not text:
        return "No text captured."
    return gemini.generate(model,text)

def show_answer_popup(answer):
    # Create a popup window to display the answer ABOVE all other windows for 10 seconds
    root = tk.Tk()
    root.title("Text Reader")
    
    screen_width = root.winfo_screenwidth()
    # Calculate the height of the popup based on the length of the answer
    answer_length = len(answer)
    height = answer_length // 2 # Adjust the height calculation as needed
    root.geometry(f"{screen_width}x{height}")
    # 200 is the height, adjust as needed
    root.configure(bg='black')
    root.attributes('-alpha', 0.7)
    root.attributes("-topmost", True)  # Ensure the window is above all other windows
    
    root.overrideredirect(True)  # Remove window border and title bar
    # Create a label to display text
    label = tk.Label(root, text=answer, font=("Helvetica", 18), fg="white", bg="black",wraplength=screen_width - 50)
    label.pack(pady=20)
    keyboard.wait('Ctrl+Shift+q')  # You can press 'Esc' to exit the program
    root.mainloop()

def on_shortcut():
    text = ocr.capture_text()
    #print(text)
    answer = generate_answer(text)
    show_answer_popup(answer)

#main
if __name__ == "__main__":
    setup()
    hotkeys_to_remove = ['ctrl+shift+1', 'ctrl+shift+x']
    
    # Remove hotkeys if they exist
    for hotkey in hotkeys_to_remove:
        if hotkey in keyboard._hotkeys:
            keyboard.remove_hotkey(hotkey)
            print(hotkey, "removed.")
    keyboard.add_hotkey('ctrl+shift+1', on_shortcut)
    print("Press 'Ctrl + Shift + 1' to capture text and get an answer.")
    print("Press 'Ctrl+Shift+X' to exit.")
    # Keep the script running to listen for the shortcut
    keyboard.wait('Ctrl+Shift+x')  # You can press 'Esc' to exit the program
    print("Program exited.")