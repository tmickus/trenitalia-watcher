# Program: Trenitalia Holiday Route Watcher
# Component: Core Checking Logic with Debugging
# File: core.py
# Version: 1.2.0
# Date: 2026-09-08

import os
import requests
import datetime


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
  print(f"\n[DEBUG] === STARTING ROUTE CHECK ===")
  print(
      f"[DEBUG] Parameters -> Origin: {origin} | Destination:"
      f" {destination} | Date: {travel_date} | Travelers: {travelers}"
  )

  try:
    target_dt = datetime.datetime.strptime(travel_date, "%Y-%m-%d").date()
    today = datetime.date.today()
    delta_days = (target_dt - today).days
    print(
        f"[DEBUG] Days between today ({today}) and target ({target_dt}):"
        f" {delta_days} days"
    )
  except Exception as date_err:
    print(f"[DEBUG] Error parsing date: {date_err}")
    delta_days = 0

  if delta_days > 120:
    msg = (
        f"[{origin} -> {destination}] ❌ No tickets available yet for"
        f" {travel_date}. It is {delta_days} days out (exceeds the ~120-day"
        " standard release window)."
    )
    print(f"[DEBUG] {msg}")
    print(f"[DEBUG] === CHECK COMPLETE (NO TICKETS LOADED) ===\n")
    return False, msg

  target_url = "https://www.trenitalia.com/"
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  print(f"[DEBUG] Querying portal endpoint: {target_url}")

  try:
    response = requests.get(target_url, headers=headers, timeout=30)
    print(f"[DEBUG] HTTP Status Code Received: {response.status_code}")
    print(f"[DEBUG] Response Body Length: {len(response.text)} characters")

    if response.status_code == 200:
      msg = (
          f"[{origin} -> {destination}] ⚠️ Portal is reachable for"
          f" {travel_date}, but direct HTML scraping requires automated"
          " session cookies or API tokens."
      )
      print(f"[DEBUG] {msg}")
      print(f"[DEBUG] === CHECK COMPLETE (PORTAL REACHABLE) ===\n")
      return True, msg
    else:
      msg = f"Check failed with status code {response.status_code}"
      print(f"[DEBUG] {msg}")
      print(f"[DEBUG] === CHECK COMPLETE (FAILED) ===\n")
      return False, msg

  except Exception as e:
    err_msg = f"Error executing check: {e}"
    print(f"[DEBUG] Exception encountered: {err_msg}")
    print(f"[DEBUG] === CHECK COMPLETE (EXCEPTION) ===\n")
    return False, err_msg