import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Developer Home", page_icon="🛠️")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "developer":
    st.warning("Please log in as a Developer from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]
username = st.session_state["username"]

st.title(f"Welcome, {username}!")
st.markdown("Your developer dashboard — manage games, view analytics, and run your studio.")

col1, col2 = st.columns(2)

with col1:
    try:
        resp = requests.get(f"{API}/developers/{user_id}/games", timeout=5)
        game_count = len(resp.json()) if resp.status_code == 200 else 0
    except Exception:
        game_count = "–"
    st.metric("My Games", game_count)

with col2:
    try:
        resp = requests.get(f"{API}/developers/{user_id}/studios", timeout=5)
        studio_count = len(resp.json()) if resp.status_code == 200 else 0
    except Exception:
        studio_count = "–"
    st.metric("Studios", studio_count)

st.divider()

col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("My Games", type="primary", use_container_width=True):
        st.switch_page("pages/21_My_Games.py")

with col_b:
    if st.button("Game Analytics", use_container_width=True):
        st.switch_page("pages/22_Game_Analytics.py")

with col_c:
    if st.button("Studio Management", use_container_width=True):
        st.switch_page("pages/23_Studio_Management.py")
