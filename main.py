import requests
import os

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

send("STATUS\n\nHTML SIZE: " + str(len(html)))

send("HAS SLOT WORD: " + str("slot" in html.lower()))

send("HAS JSON FIELD: " + str("nearest_appointment_express_datetime" in html))
