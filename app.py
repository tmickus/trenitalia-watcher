# Program: Trenitalia Holiday Route Watcher
# Component: Streamlit Web UI Dashboard
# File: app.py
# Version: 1.0.0
# Date: 2026-09-08

import streamlit as st
from core import check_train_route

st.set_page_config(
    page_title="Trenitalia Route Watcher", page_icon="🚆", layout="centered"
)

st.title("🚆 Trenitalia Holiday Schedule Watcher")
st.write(
    "Monitor winter holiday ticket releases and test route availability"
    " on-demand."
)

st.subheader("Route Parameters")
origin = st.text_input("Departure Station", value="Salerno")
destination = st.text_input("Arrival Station", value="Catania Centrale")
travel_date = st.date_input(
    "Travel Date", value=__import__("datetime").date(2026, 12, 23)
)
travelers = st.number_input(
    "Number of Travelers", min_value=1, max_value=50, value=14
)

if st.button("Run Live Check Now", type="primary"):
  with st.spinner("Querying Trenitalia endpoints..."):
    success, message = check_train_route(
        origin=origin,
        destination=destination,
        travel_date=str(travel_date),
        travelers=str(travelers),
    )
    if success:
      st.success(message)
    else:
      st.error(message)

st.markdown("---")
st.caption(
    "Background polling runs hourly via GitHub Actions to push notifications"
    " straight to Telegram."
)