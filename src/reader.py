import tkinter as tk
import time

def destroy(event=None):
    global interrupt
    interrupt = True
            
def display_text(root,label,script):
    global interrupt
    interrupt = False
    # Split the script into lines on fullstop and new line
    script=script.replace('\n','.')
    scriptlist = script.split(".")
    # words = script.split()
    # scriptlist = [' '.join(words[i:i+8]) for i in range(0, len(words), 8)]
   
    root.bind('<Control-period>', destroy)  # Press 'Ctrl + .' to interrupt
     # Loop through the text and display one at a time
    for line in scriptlist:
        if interrupt:
            break
        label.config(text=line.strip())  # Update label text
        root.update() 
        #words=line.split(' ')  
        #print(words)
        #print(int(len(words)/2))      # Update the GUI
        if interrupt:
            break
        time.sleep(int(len(line)/11))            # Display each line for 2 seconds 

def display(script):
    # Create a simple GUI window using Tkinter
    root = tk.Tk()
    root.title("Text Reader")
    
    screen_width = root.winfo_screenwidth()
    root.geometry(f"{screen_width}x100+0+0")  # 200 is the height, adjust as needed
    root.configure(bg='black')
    root.attributes('-alpha', 0.7)
    root.attributes("-topmost", True)  # Ensure the window is above all other windows
    
    root.overrideredirect(True)  # Remove window border and title bar
    # Create a label to display text
    label = tk.Label(root, text="", font=("Helvetica", 18), fg="white", bg="black",wraplength=screen_width - 50)
    label.pack(pady=20)
    
    # Start displaying text
    root.after(1000, display_text(root, label,script))  # Delay the start by 1 second

    
    #root.mainloop() # use this if you want to keep the window open

if __name__ == "__main__":
    script = """This is the first line of the script. This is the second line of the script. This is the third line of the script. This is the fourth line of the script. This is the fifth line of the script."""
    display(script)
    exit()    
