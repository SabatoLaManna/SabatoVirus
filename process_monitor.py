import psutil
import time
import requests

# Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1342178631107084358/_Aood1Po6hX3Z_Gw-EeyJRoZD9VfC_WB7VBZoaIeXQSY0WrhC9OxMjbg27XU3fvD4jTq"

# Monitor running processes every 5 seconds
try:
    while True:
        for proc in psutil.process_iter(["pid", "name"]):
            payload = {"content": f"Process: {proc.info}"}
            requests.post(WEBHOOK_URL, json=payload)
        time.sleep(5)
except KeyboardInterrupt:
    print("Process monitoring stopped.")