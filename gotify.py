import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOTIFY_URL = os.getenv("GOTIFY_URL")
APP_TOKEN = os.getenv("APP_TOKEN")

def send_gotify(message: str, title: str = "Notification", priority: int = 5):
    url = f"{GOTIFY_URL}/message"
    headers = {
        "X-Gotify-Key": APP_TOKEN
    }
    data = {
        "title": title,
        "message": message,
        "priority": priority
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

if __name__ == "__main__":
    send_gotify(
        title="Matchweek Job",
        message="MW5 processing completed successfully",
        priority=8
    )
