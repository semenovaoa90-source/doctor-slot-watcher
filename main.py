import os
import re
import requests

URL = "https://prodoctorov.ru/nnovgorod/vrach/1032093-ivanova/"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers, timeout=30)
html = r.text

m = re.search(
    r'"nearest_appointment_express_datetime":"([^"]+)"',
    html
)

if m:
    text = (
        "Найдена ближайшая запись:\n"
        + m.group(1)
        + "\n\n"
        + URL
    )
else:
    text = "Поле nearest_appointment_express_datetime не найдено."

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": text
    },
    timeout=20,
)
