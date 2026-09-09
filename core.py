import os
import requests


def send_telegram_alert(message):
  token = os.environ.get("TELEGRAM_BOT_TOKEN")
  chat_id = os.environ.get("TELEGRAM_CHAT_ID")
  if not token or not chat_id:
    print("Telegram credentials missing.")
    return
  url = f"https://api.telegram.org/bot{token}/sendMessage"
  payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
  requests.post(url, json=payload)


def check_train_route(
    origin="Salerno",
    destination="Catania Centrale",
    travel_date="2026-12-23",
    travelers="14",
):
  print(
      f"Checking availability: {origin} -> {destination} on {travel_date}"
      f" ({travelers} travelers)..."
  )
  target_url = "https://www.trenitalia.com/"
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }

  try:
    response = requests.get(target_url, headers=headers, timeout=30)
    if response.status_code == 200:
      msg = f"[{origin} -> {destination}] Portal reachable for {travel_date}."
      print(msg)
      return True, msg
    else:
      msg = f"Check failed with status code {response.status_code}"
      print(msg)
      return False, msg
  except Exception as e:
    err_msg = f"Error executing check: {e}"
    print(err_msg)
    return False, err_msg