
from celery import Celery

celery = Celery('telegram_bot', broker='redis://localhost:6379/0')

@celery.task
def send_message(chat_id, text):
    # Logic to send a message to a Telegram chat
    print(f"Sending message to {chat_id}: {text}")

@celery.task
def fetch_updates():
    # Logic to fetch updates from Telegram
    print("Fetching updates from Telegram")