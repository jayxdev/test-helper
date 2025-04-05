import json
import threading
import tkinter as tk
from vosk import Model, KaldiRecognizer
import pyaudio

class RealTimeCaption:
	def __init__(self, model_path):
		self.p = pyaudio.PyAudio()
		self.model = Model(model_path)
		input_device_index = None
		for i in range(self.p.get_device_count()):
			dev = self.p.get_device_info_by_index(i)
			if "Stereo Mix" in dev['name'] or "Loopback" in dev['name']:
				input_device_index = i
				break
		if input_device_index is None:
			print("Stereo Mix or Loopback device not found.")
			exit()

		try:
			# Open the stream
			self.stream = self.p.open(format=pyaudio.paInt16,
									  channels=1,
									  rate=48000,  # Adjusted to match recognizer's sample rate
									  input=True,
									  input_device_index=input_device_index,
									  frames_per_buffer=1024)
		except OSError as e:
			print(f"Failed to open stream: {e}")
			exit()

		print("Listening to system audio...")
		self.rec = KaldiRecognizer(self.model, 48000)
		self.start_listening()

	def listen_system_audio(self):
		while True:
			try:
				data = self.stream.read(4000, exception_on_overflow=False)
				if self.rec.AcceptWaveform(data):
					result = self.rec.Result()
					result_dict = json.loads(result)
					self.caption(result_dict.get('text', ''))
				else:
					partial_result = self.rec.PartialResult()
					result_dict = json.loads(partial_result)
					self.caption(result_dict.get('partial', ''))
			except OSError as e:
				print(f"Error reading from stream: {e}")
				break

	def start_listening(self):
		listener_thread = threading.Thread(target=self.listen_system_audio)
		listener_thread.daemon = True
		listener_thread.start()

	def caption(self, text):
		print(text)

# Example usage
if __name__ == "__main__":
	model_path = "./src/vosk-model-small-en-us-0.15"  # Replace with the actual model path
	rtc = RealTimeCaption(model_path)
	root = tk.Tk()
	root.title("Real-Time Captioning")

	text_widget = tk.Text(root, wrap='word', height=20, width=80)
	text_widget.pack(expand=True, fill='both')

	def update_caption(text):
		text_widget.insert(tk.END, text + '\n')
		text_widget.see(tk.END)

	rtc.caption = update_caption

	root.mainloop()
