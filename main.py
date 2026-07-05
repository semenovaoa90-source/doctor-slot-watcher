import requests
import os

URL = "https://prodoctorov.ru/nnovgorod/vrach/1032093-ivanova/"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text},
        timeout=20
    )

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)

html = r.text

# просто проверяем, что реально приходит со страницы
checks = {
    "has_slots": "has_slots" in html,
    "nearest": "nearest_appointment_express_datetime" in html,
    "slot_word": "slot" in html.lower(),
    "len": len(html)
}

send(
    "DEBUG ПРОДОКТОРОВ\n\n"
    + "\n".join([f"{k}: {v}" for k, v in checks.items()])
)
