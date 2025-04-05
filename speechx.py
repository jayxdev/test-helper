#main copy with keyboard
from src.profile_1 import Profile
import keyboard
from src import gemini
import threading
import src.reader as reader
import src.ocr as ocr

promt="extract speaking test question and give only plain text response which i can speak for 45seconds , remove any formating and tips"
model=gemini.setup()
def setup():
    text = "hi"
    gemini.generate(model,text)
    response = gemini.generate(model, text)
    if not response:
        print("Failed to setup the model.")
    else:
        print("Model setup complete.")

def on_shortcut(vc):
    text = ""
    if vc:
        text = ocr.capture_live_text()
    else:
        text = ocr.capture_text()
    answer = gemini.generate(model, promt+text)
    # show_answer_popup(answer)
    # Create a new thread
    thread = threading.Thread(target=reader.display, args=(answer,))
    # Start the thread
    thread.start()
    

#main
if __name__ == "__main__":
    setup()
    keyboard.add_hotkey('ctrl+/', on_shortcut,args=[True])
    print("Press 'Ctrl +/' for interview")
    
    #for swar
    keyboard.add_hotkey('Ctrl + shift + 1', on_shortcut,args=[False])
    print("Press 'Ctrl + shift + 1' for speechx")
    print("Press 'Ctrl + .' for reader interrupt")

    # Keep the script running to listen for the shortcut
    keyboard.wait('Ctrl+Shift+x')  # You can press 'Esc' to exit the program
    print("Program exited.")

    