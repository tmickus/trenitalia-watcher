import os
import requests

ORIGIN = os.environ.get("ORIGIN", "Salerno")
DESTINATION = os.environ.get("DESTINATION", "Catania Centrale")
TRAVEL_DATE = os.environ.get("TRAVEL_DATE", "2026-12-23")
TRAVELERS = os.environ.get("TRAVELERS", "14")


def send_telegram_alert(message):
  token = os.environ.get("TELEGRAM_BOT_TOKEN")
  chat_id = os.environ.get("TELEGRAM_CHAT_ID")
  url = f"https://api.telegram.org/bot{token}/sendMessage"
  payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
  requests.post(url, json=payload)


def check_route():
  print(
      f"Checking availability for: {ORIGIN} -> {DESTINATION} on"
      f" {TRAVEL_DATE} for {TRAVELERS} travelers..."
  )
  target_url = "https://www.trenitalia.com/"
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }

  try:
    response = requests.get(target_url, headers=headers, timeout=30)
    if response.status_code == 200:
      print(f"[{ORIGIN} -> {DESTINATION}] Portal reachable.")
      # send_telegram_alert(f"🚨 *Train Alert:* Tickets live for {ORIGIN} to {DESTINATION} on {TRAVEL_DATE} ({TRAVELERS} pax)!")
    else:
      print(f"Check failed with status {response.status_code}")
  except Exception as e:
    print(f"Error checking route: {e}")


if __name__ == "__main__":
  check_route()