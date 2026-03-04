import requests
from app.config import settings

def send_telegram_alert(product_name: str, current_price: float, target_price: float):
    message = (
        f"🔔 Price Alert!\n"
        f"Product: {product_name}\n"
        f"Current price: R${current_price}\n"
        f"Target price: R${target_price}\n"
        f"The product has reached your target price!"
    )
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message
    })