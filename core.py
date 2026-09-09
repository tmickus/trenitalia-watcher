# Program: Trenitalia Holiday Route Watcher
# Component: Core Checking Logic with Strict JSON Fallback
# File: core.py
# Version: 1.3.4
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
  
  try:
    target_dt = datetime.datetime.strptime(travel_date, "%Y-%m-%d").date()
    today = datetime.date.today()
    delta_days = (target_dt - today).days
  except Exception as date_err:
    print(f"[DEBUG] Error parsing date: {date_err}")
    delta_days = 0

  if delta_days > 120:
    msg = (
        f"[{origin} -> {destination}] ❌ No tickets available yet for"
        f" {travel_date}. It is {delta_days} days out (exceeds the ~120-day"
        " standard release window)."
    )
    return False, msg

  formatted_date = target_dt.strftime("%d/%m/%Y 0:00:00")
  api_url = "https://www.lefrecce.it/msite/api/solutions"

  params = {
      "origin": origin,
      "destination": destination,
      "arflag": "A",
      "adate": formatted_date,
      "atime": "8",
      "adultno": str(travelers),
      "childno": "0",
      "direction": "A",
      "frecce": "false",
      "onlyRegional": "false",
  }

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      ),
      "Accept": "application/json",
  }

  try:
    response = requests.get(api_url, params=params, headers=headers, timeout=30)
    
    # 1. Check if the response is completely empty (this is what caused the crash)
    if not response.text or not response.text.strip():
        msg = f"[{origin} -> {destination}] 🛡️ Server dropped the request (Empty response returned)."
        return False, msg

    # 2. Attempt to parse JSON safely
    try:
        data = response.json()
    except ValueError:
        msg = f"[{origin} -> {destination}] 🛡️ Server blocked API request. Received non-JSON: {response.text[:100]}"
        return False, msg

    # 3. Process valid data
    solutions = data if isinstance(data, list) else data.get("solutions", [])

    if solutions:
      msg = f"[{origin} -> {destination}] ✅ Found {len(solutions)} train options for {travel_date}!"
      return True, msg
    else:
      msg = f"[{origin} -> {destination}] ⏳ Portal reachable for {travel_date}, but zero solutions returned (tickets not yet loaded/released)."
      return False, msg

  except Exception as e:
    return False, f"Error executing check: {e}"