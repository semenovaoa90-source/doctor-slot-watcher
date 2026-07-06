import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://prodoctorov.ru/nnovgorod/vrach/1032093-ivanova/"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg[:4000]}
    )

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, timeout=60000)
    page.wait_for_timeout(5000)

    html = page.content()
    browser.close()

if "запис" in html.lower() or "slot" in html.lower():
    send("Страница загрузилась, есть данные (проверка успешна)")
else:
    send("Слоты не найдены или не загружены")
