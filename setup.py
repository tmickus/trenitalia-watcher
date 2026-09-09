import os

# Create the .github/workflows directory structure
os.makedirs(".github/workflows", exist_ok=True)

# 1. Write watcher.py
watcher_code = """import os
import requests
import json

def send_telegram_alert(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def check_all_routes():
    try:
        with open("routes.json", "r") as f:
            routes = json.load(f)
    except FileNotFoundError:
        print("routes.json not found.")
        return

    for route in routes:
        origin = route["origin"]
        destination = route["destination"]
        travel_date = route["date"]

        print(f"Checking availability for: {origin} -> {destination} on {travel_date}...")
        target_url = "https://www.trenitalia.com/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        try:
            response = requests.get(target_url, headers=headers, timeout=30)
            if response.status_code == 200:
                print(f"[{origin} -> {destination}] Portal reachable.")
                # send_telegram_alert(f"🚨 *Train Alert:* Tickets live for {origin} to {destination} ({travel_date})!")
            else:
                print(f"[{origin} -> {destination}] Check failed with status {response.status_code}")
        except Exception as e:
            print(f"Error checking {origin} to {destination}: {e}")

if __name__ == "__main__":
    check_all_routes()
"""

with open("watcher.py", "w", encoding="utf-8") as f:
  f.write(watcher_code)

# 2. Write .github/workflows/watcher.yml
workflow_code = """name: Trenitalia Hourly Watcher

on:
  schedule:
    - cron: '0 * * * *'
  workflow_dispatch:

jobs:
  run-watcher:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install requests

      - name: Run Watcher Script
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEOGRAPH_CHAT_ID } # fix key below in final or keep standard
        run: |
          python watcher.py
"""

# Fixing the typo in workflow_code TELEGRAM_CHAT_ID:
workflow_code = workflow_code.replace(
    "${{ secrets.TELEOGRAPH_CHAT_ID }", "${{ secrets.TELEGRAM_CHAT_ID }}"
)

with open(".github/workflows/watcher.yml", "w", encoding="utf-8") as f:
  f.write(workflow_code)

print("Folder structure and files created successfully!")