import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
import sys
import subprocess
import keyboard
import threading

SERVICE_NAME = "CheatService"

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = "Auto Cheat Service"
    _svc_description_ = "This service runs a Python script in the background."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_event = threading.Event()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop_event.set()

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # Path to your main script
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        subprocess.Popen([sys.executable, script_path])

        # Start a separate thread for hotkey listening
        print("Starting hotkey listener thread...")
        hotkey_thread = threading.Thread(target=self.listen_for_hotkeys)
        hotkey_thread.start()

        # Wait for stop event
        print("Waiting for stop event...")
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

        # Clean up
        print("Stopping hotkey listener thread...")
        self.stop_event.set()
        hotkey_thread.join()

        print("Service stopped.")

    def listen_for_hotkeys(self):
        try:
            # Register hotkey to start/stop the service
            print("Registering hotkey...")
            keyboard.add_hotkey('ctrl+shift+x', self.toggle_service)
            print("Hotkey registered. Press 'Ctrl + Shift + X' to start/stop the service. Press 'Esc' to exit.")

            # Keep the script running to listen for the hotkey
            while not self.stop_event.is_set():
                keyboard.wait('esc')  # You can press 'Esc' to exit the program

            print("Hotkey listener stopped.")
        except Exception as e:
            print(f"Exception in hotkey listener: {e}")

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