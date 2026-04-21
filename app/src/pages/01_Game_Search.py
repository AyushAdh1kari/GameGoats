import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Game Search", page_icon="🔍")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "player":
    st.warning("Please log in as a Player from the Home page.")
    st.stop()

API = "http://web-api:4000"

st.title("Game Search")

search_query = st.text_input("Search by title", placeholder="e.g. Crimson Frontier")

with st.expander("Filters", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        try:
            resp = requests.get(f"{API}/tags", timeout=5)
            all_tags = [t["tag_name"] for t in resp.json()] if resp.status_code == 200 else []
        except Exception:
            all_tags = []
        selected_tags = st.multiselect("Tags", all_tags)

    with col2:
        genres = ["Shooter", "RPG", "Strategy", "Simulation", "Sports",
                  "Adventure", "Puzzle", "Platformer", "Racing", "Horror"]
        selected_genres = st.multiselect("Genre", genres)

    with col3:
        platforms = ["PC", "PlayStation", "Xbox", "Nintendo", "Mobile"]
        selected_platform = st.selectbox("Platform", ["All"] + platforms)

try:
    resp = requests.get(f"{API}/games", timeout=5)
    games = resp.json() if resp.status_code == 200 else []
except Exception:
    games = []
    st.error("Could not reach the API.")

if search_query:
    games = [g for g in games if search_query.lower() in g.get("title", "").lower()]
if selected_genres:
    games = [g for g in games if g.get("genre") in selected_genres]
if selected_platform and selected_platform != "All":
    games = [g for g in games if g.get("platform") == selected_platform]
if selected_tags:
    filtered = []
    for g in games:
        try:
            tag_resp = requests.get(f"{API}/games/{g['game_id']}/tags", timeout=3)
            game_tags = [t["tag_name"] for t in tag_resp.json()] if tag_resp.status_code == 200 else []
            if any(t in game_tags for t in selected_tags):
                filtered.append(g)
        except Exception:
            filtered.append(g)
    games = filtered

st.markdown(f"**{len(games)} games found**")

if games:
    for g in games:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
            with c1:
                st.markdown(f"**{g.get('title', 'Untitled')}**")
            with c2:
                st.caption(f"{g.get('genre', '')} · {g.get('platform', '')}")
            with c3:
                rating = g.get("average_rating", 0)
                if isinstance(rating, str):
                    rating = float(rating)
                st.caption(f"⭐ {rating:.1f}")
            with c4:
                if st.button("View", key=f"view_{g['game_id']}", use_container_width=True):
                    st.session_state["selected_game_id"] = g["game_id"]
                    st.switch_page("pages/02_Game_Detail.py")
else:
    st.info("No games match your search criteria.")
