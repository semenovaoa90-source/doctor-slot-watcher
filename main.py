import traceback

print("СТАРТ")

try:
    import os
    import requests

    print("IMPORT OK")
    print("BOT:", repr(os.getenv("BOT_TOKEN")))
    print("CHAT:", repr(os.getenv("CHAT_ID")))

    r = requests.get("https://prodoctorov.ru/nnovgorod/vrach/1032093-ivanova/", timeout=30)

    print("STATUS:", r.status_code)
    print("LEN:", len(r.text))

except Exception:
    traceback.print_exc()
