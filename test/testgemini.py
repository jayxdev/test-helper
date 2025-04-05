# Import the Python SDK
import google.generativeai as genai

GOOGLE_API_KEY="AIzaSyD_JLFtabbujqdLsmSACpdHOHyTBmHL4fQ"

#service
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
import sys
import subprocess
import keyboard

SERVICE_NAME = "CheastService"

class MyService(win32serviceutil.ServiceFramework):
	_svc_name_ = SERVICE_NAME
	_svc_display_name_ = "Auto Cheat Service"
	_svc_description_ = "This service runs a Python script in the background."

	def __init__(self, args):
		win32serviceutil.ServiceFramework.__init__(self, args)
		self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
		socket.setdefaulttimeout(60)

	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		win32event.SetEvent(self.hWaitStop)

	def SvcDoRun(self):
		servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
							  servicemanager.PYS_SERVICE_STARTED,
							  (self._svc_name_, ''))
		self.main()

	def main(self):
		# Path to your main script
		script_path = os.path.join(os.path.dirname(__file__), "main.py")
		subprocess.Popen([sys.executable, script_path])

		# Register hotkey to start/stop the service
		keyboard.add_hotkey('ctrl+shift+x', self.toggle_service)
		print("Press 'Ctrl + Shift + X' to start/stop the service. Press 'Esc' to exit.")

		# Keep the script running to listen for the hotkey
		keyboard.wait('esc')  # You can press 'Esc' to exit the program

		print("Program exited.")

	def toggle_service(self):
		try:
			result = subprocess.run(["sc", "query", SERVICE_NAME], capture_output=True, text=True, check=True)
			if "RUNNING" in result.stdout:
				self.stop_service()
			else:
				self.start_service()
		except subprocess.CalledProcessError as e:
			print(f"Failed to query service {SERVICE_NAME}: {e}")

	def start_service(self):
		try:
			subprocess.run(["sc", "start", SERVICE_NAME], check=True)
			print(f"Service {SERVICE_NAME} started.")
		except subprocess.CalledProcessError as e:
			print(f"Failed to start service {SERVICE_NAME}: {e}")

	def stop_service(self):
		try:
			subprocess.run(["sc", "stop", SERVICE_NAME], check=True)
			print(f"Service {SERVICE_NAME} stopped.")
		except subprocess.CalledProcessError as e:
			print(f"Failed to stop service {SERVICE_NAME}: {e}")

if __name__ == '__main__':
	win32serviceutil.HandleCommandLine(MyService)



#main copy with keyboard
import pytesseract
import keyboard
from tkinter import Tk, Label
from PIL import ImageGrab
import google.generativeai as genai
from src.autotyper import type_from_clipboard

# Path to your Tesseract executable (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
GOOGLE_API_KEY="AIzaSyD_JLFtabbujqdLsmSACpdHOHyTBmHL4fQ"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
def setup():
    response = model.generate_content("extract mcq and return only answer to the mcq question")
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
    # Close the window after 10 seconds
    root.after(3000, root.destroy)
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
    print(answer)
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