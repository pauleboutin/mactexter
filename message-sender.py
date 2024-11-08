import pandas as pd
import subprocess
import time
from typing import List, Tuple
import tkinter as tk
from tkinter import ttk

class MessageSender:
    def __init__(self, csv_path: str):
        # Read CSV/Excel file
        self.df = pd.read_csv(csv_path) if csv_path.endswith('.csv') else pd.read_excel(csv_path)
        self.current_index = 0
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Message Sender")
        self.root.geometry("600x400")

        # Message preview frame
        preview_frame = ttk.LabelFrame(self.root, text="Current Message", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.to_label = ttk.Label(preview_frame, text="To:")
        self.to_label.pack(anchor=tk.W)
        self.to_field = ttk.Label(preview_frame, text="")
        self.to_field.pack(anchor=tk.W)

        self.message_label = ttk.Label(preview_frame, text="Message:")
        self.message_label.pack(anchor=tk.W)
        self.message_field = ttk.Label(preview_frame, wraplength=550, justify=tk.LEFT)
        self.message_field.pack(anchor=tk.W, fill=tk.X)

        # Progress frame
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress_label = ttk.Label(progress_frame, text="Progress: 0/0")
        self.progress_label.pack(side=tk.LEFT)

        # Button frame
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        self.send_button = ttk.Button(button_frame, text="Send", command=self.send_current)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.skip_button = ttk.Button(button_frame, text="Skip", command=self.next_message)
        self.skip_button.pack(side=tk.LEFT, padx=5)

        # Load first message
        self.update_display()

    def send_message(self, phone: str, message: str) -> bool:
        """Send message using Apple Messages via AppleScript"""
        script = f'''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{phone}" of targetService
            send "{message}" to targetBuddy
        end tell
        '''
        try:
            subprocess.run(['osascript', '-e', script], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def update_display(self):
        if self.current_index < len(self.df):
            row = self.df.iloc[self.current_index]
            self.to_field.config(text=row['phone'])  # Adjust column name as needed
            self.message_field.config(text=row['message'])  # Adjust column name as needed
            self.progress_label.config(text=f"Progress: {self.current_index + 1}/{len(self.df)}")
            self.send_button.config(state=tk.NORMAL)
        else:
            self.to_field.config(text="Complete!")
            self.message_field.config(text="All messages processed")
            self.send_button.config(state=tk.DISABLED)

    def send_current(self):
        if self.current_index < len(self.df):
            row = self.df.iloc[self.current_index]
            if self.send_message(row['phone'], row['message']):  # Adjust column names as needed
                self.next_message()
            else:
                tk.messagebox.showerror("Error", "Failed to send message")

    def next_message(self):
        self.current_index += 1
        self.update_display()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Replace with your CSV/Excel file path
    sender = MessageSender("messages.csv")
    sender.run()
