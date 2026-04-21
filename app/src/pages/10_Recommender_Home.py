import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Recommender Home", page_icon="💡")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "recommender":
    st.warning("Please log in as a Recommender from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]
username = st.session_state["username"]

st.title(f"Welcome, {username}!")
st.markdown("Your recommender dashboard — review games, manage recommendations, and engage in forums.")

col1, col2 = st.columns(2)

with col1:
    try:
        resp = requests.get(f"{API}/users/{user_id}/recommendations", timeout=5)
        recs = resp.json() if resp.status_code == 200 else []
        new_count = sum(1 for r in recs if r.get("recommendation_status") == "new")
    except Exception:
        recs = []
        new_count = "–"
    st.metric("Pending Recommendations", new_count)

with col2:
    try:
        saved_count = sum(1 for r in recs if r.get("is_saved"))
    except Exception:
        saved_count = "–"
    st.metric("Saved for Later", saved_count)

st.divider()

col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("Recommendation Feed", type="primary", use_container_width=True):
        st.switch_page("pages/11_Recommendation_Feed.py")

with col_b:
    if st.button("Game Reviews", use_container_width=True):
        st.switch_page("pages/12_Game_Reviews.py")

with col_c:
    if st.button("Forum Threads", use_container_width=True):
        st.switch_page("pages/13_Forum_Threads.py")
