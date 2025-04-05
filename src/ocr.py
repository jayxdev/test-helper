from PIL import ImageGrab
import pygetwindow as gw
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_live_text():
    window = gw.getWindowsWithTitle("Live Captions")
    if not window:
        print(f"Window with title Live Captions not found.")
        return ""
        
    window = window[0]  # Get the first window that matches the title
    
        # Get the window's bounding box
    bbox = (window.left, window.top, window.right, window.bottom)
    # Capture the entire screen (you can modify this to capture a specific region)
    img = ImageGrab.grab(bbox=bbox)  
    # Use OCR to extract text from the captured image
    text = pytesseract.image_to_string(img)
    
    # Return the captured text
    return text.strip()

def capture_text():
    # Capture the entire screen (you can modify this to capture a specific region)
    #grab the screen leaving head of chrome
    # Capture the entire screen except the top part occupied by Chrome
    img = ImageGrab.grab()
    # Use OCR to extract text from the captured image
    text = pytesseract.image_to_string(img)
    # Return the captured text
    return text.strip()

if __name__ == "__main__":
    text = capture_text()
    print(text)
    # text = capture_live_text()
    # print(text)