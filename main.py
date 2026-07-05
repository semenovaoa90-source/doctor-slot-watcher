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
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


def fetch_page():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(URL, headers=headers, timeout=20)
    return r.text


def extract_slots(html):
    soup = BeautifulSoup(html, "html.parser")

    # убираем лишние пробелы и приводим к одному тексту
    text = " ".join(soup.stripped_strings).lower()

    # реальные признаки доступной записи
    # (под ProDoctorov обычно встречается именно "свободно" + даты/время)
    keywords = ["свободно", "запись", "записаться", "выбрать дату", "время приема"]

    found = []

    for k in keywords:
        if k in text:
            found.append(k)

    # дополнительно: пытаемся вытащить куски с датами/временем
    # (очень грубая, но рабочая эвристика)
    for part in text.split():
        if ":" in part and len(part) <= 5:
            found.append(part)

    return list(set(found))


def main():
    state = load_state()

    html = fetch_page()
    slots = extract_slots(html)

    # если вообще ничего не найдено — выходим тихо
    if not slots:
        return

    # проверка на новые события
    new_slots = [s for s in slots if s not in state["slots"]]

    if new_slots:
        message = (
            "🔔 Найдены изменения в записи к врачу\n\n"
            f"{URL}\n\n"
            "Детали:\n- " + "\n- ".join(new_slots)
        )
        send_telegram(message)

        state["slots"] = slots
        save_state(state)


if __name__ == "__main__":
    main()
