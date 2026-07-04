import os
import json
import requests
from bs4 import BeautifulSoup

URL = "https://prodoctorov.ru/nnovgorod/vrach/1032093-ivanova/"
STATE_FILE = "state.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"slots": []}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })


def fetch_page():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(URL, headers=headers, timeout=20)
    return r.text


def extract_slots(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True).lower()

    keywords = ["записаться", "свободно", "есть запись", "выбрать время"]

    slots_found = []
    for kw in keywords:
        if kw in text:
            slots_found.append(kw)

    return slots_found


def main():
    state = load_state()

    html = fetch_page()
    slots = extract_slots(html)

    new_slots = [s for s in slots if s not in state["slots"]]

    if new_slots:
        message = (
            "🔔 Найдена запись к врачу\n\n"
            f"Ссылка: {URL}\n"
            f"Детали: {', '.join(new_slots)}"
        )
        send_telegram(message)

        state["slots"] = slots
        save_state(state)


if __name__ == "__main__":
    main()
