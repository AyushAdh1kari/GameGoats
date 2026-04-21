import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Player Home", page_icon="🎮")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "player":
    st.warning("Please log in as a Player from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]
username = st.session_state["username"]

st.title(f"Welcome, {username}!")
st.markdown("Your player dashboard — browse games, check your profile, and explore the community.")

col1, col2, col3 = st.columns(3)

with col1:
    try:
        resp = requests.get(f"{API}/users/{user_id}/favorites", timeout=5)
        fav_count = len(resp.json()) if resp.status_code == 200 else 0
    except Exception:
        fav_count = "–"
    st.metric("Favorites", fav_count)

with col2:
    try:
        resp = requests.get(f"{API}/users/{user_id}/comments", timeout=5)
        review_count = len(resp.json()) if resp.status_code == 200 else 0
    except Exception:
        review_count = "–"
    st.metric("Reviews Written", review_count)

with col3:
    try:
        resp = requests.get(f"{API}/users/{user_id}/follows", timeout=5)
        follow_count = len(resp.json()) if resp.status_code == 200 else 0
    except Exception:
        follow_count = "–"
    st.metric("Following", follow_count)

st.divider()

col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("Search Games", type="primary", use_container_width=True):
        st.switch_page("pages/01_Game_Search.py")

with col_b:
    if st.button("Game Detail", use_container_width=True):
        st.switch_page("pages/02_Game_Detail.py")

with col_c:
    if st.button("My Profile", use_container_width=True):
        st.switch_page("pages/03_My_Profile.py")
