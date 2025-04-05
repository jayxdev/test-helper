import tkinter as tk
from tkinter import scrolledtext

# Function to send the message
class ChatWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WhatsApp-like Chat Window")
        self.root.geometry("400x500")
        
        # Create the chat area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='normal')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Configure tags for different message types
        self.chat_area.tag_configure("user", foreground="green", justify='right')
        self.chat_area.tag_configure("other", foreground="blue", justify='left')
        
        # # Create the message entry box
        # message_entry = tk.Entry(self.root)
        # message_entry.pack(padx=10, pady=10, fill=tk.X)
        # #message_entry.bind("<Return>", send_message(message_entry,chat_area))
        
        # Create the send button
        #send_button = tk.Button(root, text="Send", command=send_message(message_entry,chat_area))
        #  send_button.pack(padx=10, pady=10)
        
    def send_message(self,message):
        #message = message_entry.get()
        #print(f"User: {message}")  # Print user's message to the console
        if message.strip():  # Only send non-empty messages
            # Display user's message on the right side in green bubble
            self.chat_area.insert(tk.END, f"User: {message}\n", "user")
            self.chat_area.see(tk.END)  # Auto-scroll to the bottom
            #message_entry.delete(0, tk.END)
            
    def receive_message(self,message):        
        # Simulate a response from another user (optional)
        self.chat_area.insert(tk.END, f"Interviewer: {message}\n", "other")
        self.chat_area.see(tk.END)  # Auto-scroll to the bottom


if __name__ == "__main__":
    chat=ChatWindow()
    chat.send_message("hi")
    chat.receive_message("hello")
    # Start the Tkinter event loop
    chat.root.mainloop()