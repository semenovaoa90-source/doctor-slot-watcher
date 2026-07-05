import os
import re
import json
import requests

URL = "https://prodoctorov.ru/nnovgorod/vrach/1032093-ivanova/"
STATE_FILE = "state.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "nearest": "",
        "has_slots": False
    }


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=20
    )


headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=headers, timeout=30).text

m_slot = re.search(r'"has_slots":(true|false)', html)
m_date = re.search(
    r'"nearest_appointment_express_datetime":"([^"]*)"',
    html
)

has_slots = False
nearest = ""

if m_slot:
    has_slots = m_slot.group(1) == "true"

if m_date:
    nearest = m_date.group(1)

state = load_state()

if (
    has_slots != state["has_slots"]
    or nearest != state["nearest"]
):
    text = (
        "🔔 Изменения записи к врачу\n\n"
        f"Свободные слоты: {'Да' if has_slots else 'Нет'}\n"
        f"Ближайшая запись: {nearest if nearest else 'нет'}\n\n"
        f"{URL}"
    )

    send_message(text)

    save_state({
        "has_slots": has_slots,
        "nearest": nearest
    })
