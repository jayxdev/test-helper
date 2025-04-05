#main copy with keyboard
from src.profile_1 import Profile
import keyboard
from src import gemini
import threading
import src.ocr as ocr
import src.chatWindow as chatWindow
import time
import speechtotext as st


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
    rtc = RealTimeCaption(model_path)
    while True:
        #listen untill big gap
        caption=rtc.listen()

    