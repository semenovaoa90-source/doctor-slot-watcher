import os
import requests

URL = "https://prodoctorov.ru/nnovgorod/vrach/1032093-ivanova/"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text[:4000]},
        timeout=20
    )

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
html = r.text

# простая проверка — меняется ли страница
if "врач" in html.lower():
    send("Бот работает. Страница доступна.\n" + URL)
else:
    send("Страница не загрузилась")
