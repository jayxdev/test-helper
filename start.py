#main copy with keyboard
import keyboard
from tkinter import Tk, Label
from PIL import ImageGrab
from src import gemini
from src.autotyper import type_from_clipboard
import src.ocr as ocr
import time

# Path to your Tesseract executable (adjust if needed)
model=gemini.setup()
def setup():
    response = gemini.generate(model,"Extract multiple-choice question (MCQs) from the provided text and return only the correct answer for MCQ, without any explanation or additional information.")
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
    root = Tk()
    root.title("Answer")
    
    # Calculate window size based on answer length
    width = min(400, max(200, len(answer) * 7)) 
    height = min(1000, max(60, len(answer) // 2)) 
    
    
    root.geometry(f"{width}x{height}")
    root.attributes("-topmost", True)  # Ensure the window is above all other windows
    root.overrideredirect(True)  # Remove window decorations
    label = Label(root, text=answer, wraplength=width - 20) 
    label.pack(pady=20)
    # Close the window after 3 seconds
    root.after(3000, root.destroy)
    root.mainloop()

def on_shortcut():
    text = ocr.capture_text()
    #print(text)
    answer = generate_answer(text)
    #copy answer to clipboard
      # Retry mechanism for clipboard access
    for _ in range(10):  # Retry up to 10 times
        try:
            root = Tk()
            root.withdraw()  # Hide the root window
            root.clipboard_clear()
            root.clipboard_append(answer)
            root.update()  # Now it stays on the clipboard after the window is closed
            root.destroy()
            break
        except Exception as e:
            print(f"Clipboard access failed: {e}. Retrying...")
            time.sleep(0.1)  # Wait for 100ms before retrying
    
    show_answer_popup(answer)

#main
if __name__ == "__main__":
    setup()
    hotkeys_to_remove = ['ctrl+shift+1', 'ctrl+shift+h', 'ctrl+shift+x']
    
    # Remove hotkeys if they exist
    for hotkey in hotkeys_to_remove:
        if hotkey in keyboard._hotkeys:
            keyboard.remove_hotkey(hotkey)
            print(hotkey, "removed.")
    keyboard.add_hotkey('ctrl+shift+1', on_shortcut)
    print("Press 'Ctrl + Shift + 1' to capture text and get an answer. Press 'Ctrl+Shift+h' to type.")
    keyboard.add_hotkey('ctrl+shift+h', type_from_clipboard)
    print("Press 'Ctrl+Shift+X' to exit.")
    # Keep the script running to listen for the shortcut
    keyboard.wait('Ctrl+Shift+x')  # You can press 'Esc' to exit the program
    print("Program exited.")