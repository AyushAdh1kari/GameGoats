import requests
import streamlit as st

from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide", page_title="Player Home", page_icon="🎮")
SideBarLinks()
user = require_persona("player")

st.title("Julia Player Home")
st.write(f"Welcome back, {user['display_name']}. Use this player workspace to explore the live game catalog and file safety reports.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Browse Games")
    st.caption("Search the current catalog and scan genres, platforms, and lifecycle state.")
    if st.button("Open Game Browser", type="primary", use_container_width=True):
        st.switch_page("pages/01_Player_Browse_Games.py")

with col2:
    st.subheader("Inspect A Game")
    st.caption("Pull a single title by id and read its full details before deciding what to play.")
    if st.button("Open Game Details", type="primary", use_container_width=True):
        st.switch_page("pages/02_Player_Game_Details.py")

with col3:
    st.subheader("Submit Report")
    st.caption("Escalate a suspicious game, player, comment, or thread through the live report API.")
    if st.button("Open Report Form", type="primary", use_container_width=True):
        st.switch_page("pages/03_Player_Submit_Report.py")

st.divider()
st.markdown(
    """
    ### Player demo flow
    1. Browse the live `GET /games` catalog.
    2. Inspect a specific title with `GET /games/<game_id>`.
    3. Submit a moderation issue with `POST /reports`.
    """
)
