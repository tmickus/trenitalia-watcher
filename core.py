# Program: Trenitalia Holiday Route Watcher
# Component: Core Checking Logic with Anti-Bot HTML Shield
# File: core.py
# Version: 1.3.3
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
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/122.0.0.0 Safari/537.36"
      ),
      "Accept": "application/json, text/plain, */*",
      "Accept-Language": "en-US,en;q=0.9,it;q=0.8",
      "Referer": "https://www.lefrecce.it/",
  }

  print(f"[DEBUG] Querying LeFrecce API endpoint with anti-bot headers...")

  try:
    response = requests.get(api_url, params=params, headers=headers, timeout=30)
    print(f"[DEBUG] HTTP Status Code Received: {response.status_code}")
    print(f"[DEBUG] Content-Type: {response.headers.get('content-type', '')}")

    # Shield against HTML block pages (Akamai/Cloudflare anti-bot challenges)
    if response.status_code != 200 or response.text.strip().startswith("<") or "application/json" not in response.headers.get("content-type", ""):
      msg = (
          f"[{origin} -> {destination}] 🛡️ Trenitalia anti-bot protection"
          " intercepted the direct script request. (Normal for server-side"
          " API queries without browser session cookies)."
      )
      print(f"[DEBUG] {msg}")
      return False, msg

    data = response.json()
    solutions = data if isinstance(data, list) else data.get("solutions", [])

    if solutions:
      msg = (
          f"[{origin} -> {destination}] ✅ Found {len(solutions)} train"
          f" options for {travel_date}!"
      )
      print(f"[DEBUG] {msg}")
      return True, msg
    else:
      msg = (
          f"[{origin} -> {destination}] ⏳ Portal reachable for"
          f" {travel_date}, but zero solutions returned (tickets not yet"
          " loaded/released)."
      )
      print(f"[DEBUG] {msg}")
      return False, msg

  except Exception as e:
    err_msg = f"Error executing check: {e}"
    print(f"[DEBUG] Exception encountered: {err_msg}")
    return False, err_msg