import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="My Games", page_icon="🎲")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "developer":
    st.warning("Please log in as a Developer from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]

st.title("My Games")

try:
    resp = requests.get(f"{API}/developers/{user_id}/games", timeout=5)
    my_games = resp.json() if resp.status_code == 200 else []
except Exception:
    my_games = []

if my_games:
    st.dataframe(
        [
            {
                "Title": g.get("title", "–"),
                "Genre": g.get("genre", "–"),
                "Platform": g.get("platform", "–"),
                "Rating": g.get("average_rating", "–"),
                "Status": g.get("lifecycle_status", "–"),
                "Release Year": g.get("release_year", "–"),
            }
            for g in my_games
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No games found for your developer profile.")

st.divider()

st.subheader("Publish a New Game")

try:
    studios_resp = requests.get(f"{API}/developers/{user_id}/studios", timeout=5)
    studios = studios_resp.json() if studios_resp.status_code == 200 else []
except Exception:
    studios = []

with st.form("publish_game_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Game Title", max_chars=128)
        genre = st.selectbox("Genre", ["Shooter", "RPG", "Strategy", "Simulation", "Sports",
                                        "Adventure", "Puzzle", "Platformer", "Racing", "Horror"])
        platform = st.selectbox("Platform", ["PC", "PlayStation", "Xbox", "Nintendo", "Mobile"])

    with col2:
        description = st.text_area("Description", max_chars=500, height=120)
        studio_options = {s.get("studio_name", f"Studio #{s['studio_id']}"): s["studio_id"] for s in studios}
        selected_studio = st.selectbox("Publishing Studio",
                                       list(studio_options.keys()) if studio_options else ["No studios found"])
        release_year = st.number_input("Release Year", min_value=2000, max_value=2030, value=2026)

    submitted = st.form_submit_button("Publish Game", type="primary")
    if submitted and title.strip() and description.strip():
        studio_id = studio_options.get(selected_studio)
        try:
            resp = requests.post(
                f"{API}/games",
                json={
                    "title": title.strip(),
                    "description": description.strip(),
                    "genre": genre,
                    "platform": platform,
                    "release_year": release_year,
                    "published_by_studio_id": studio_id,
                    "developer_id": user_id,
                },
                timeout=5,
            )
            if resp.status_code == 201:
                st.success(f"Game '{title}' published!")
                st.rerun()
            else:
                st.error(f"Failed: {resp.text}")
        except Exception as e:
            st.error(f"API error: {e}")
    elif submitted:
        st.warning("Please fill in both title and description.")
