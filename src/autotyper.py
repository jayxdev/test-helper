"""types whats in the clipboard"""

import pyautogui
import time
import win32clipboard

def type_from_clipboard():
    # Get text from clipboard
    win32clipboard.OpenClipboard()
    clipboard_text = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    # Wait for user to focus on the desired input field
    time.sleep(5)

    # Type the text from clipboard
    pyautogui.typewrite(clipboard_text)

# Call the function to type the text from clipboard
if __name__ == "__main__":
    type_from_clipboard()