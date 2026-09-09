# Program: Trenitalia Holiday Route Watcher
# Component: Background Automation Worker
# File: watcher.py
# Version: 1.1.0
# Date: 2026-09-08

import os
from core import check_train_route

if __name__ == "__main__":
  origin = os.environ.get("ORIGIN", "Salerno")
  destination = os.environ.get("DESTINATION", "Catania Centrale")
  travel_date = os.environ.get("TRAVEL_DATE", "2026-12-23")
  travelers = os.environ.get("TRAVELERS", "14")

  check_train_route(
      origin=origin,
      destination=destination,
      travel_date=travel_date,
      travelers=travelers,
  )