import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# --- General Utility Tool (Pushover) ---
def push(text):
    """Sends a notification to Pushover."""
    token = os.getenv("PUSHOVER_TOKEN")
    user = os.getenv("PUSHOVER_USER")
    if not token or not user:
        print("Pushover API keys not set in .env. Skipping notification.")
        return
    
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": token,
            "user": user,
            "message": text,
        }
    )
