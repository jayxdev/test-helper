#main copy with keyboard
from src.profile_1 import Profile
import keyboard
from src import gemini
import threading
import src.ocr as ocr
import src.chatWindow as chatWindow
import time

model=gemini.setup()
def setup():
    #text = "extract interview question from further inputs and give only response which i can speak directly to the interviewer remove tips and all"
    #gemini.generate(model, Profile)
    response = gemini.generate(model, "text")
    if not response:
        print("Failed to setup the model.")
    else:
        print("Model setup complete.")


#main
if __name__ == "__main__":
    #setup()
    history=[]
    chat=chatWindow.ChatWindow()
    while True:
        time.sleep(2)
        text = ocr.capture_live_text()
        print(text)
        if text.strip() not in history and text.strip():
            history.append(text.strip())
            chat.send_message(text.strip())
            #answer = gemini.generate(model, text)
            answer ="sample text"
            chat.receive_message(answer)
        chat.root.update_idletasks()
        chat.root.update()
    