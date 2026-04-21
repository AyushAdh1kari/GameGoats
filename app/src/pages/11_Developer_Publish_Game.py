import streamlit as st

from modules.api_client import get_json, post_json
from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
require_persona("developer")

st.title("Publish Game")
st.write("Create a new catalog entry using the live `POST /games` endpoint.")

games, error, _ = get_json("/games")
if error:
    st.error(error)
    st.stop()

st.metric("Current Catalog Size", len(games))

with st.form("publish_game_form"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    genre = st.selectbox("Genre", ["Adventure", "Puzzle", "RPG", "Shooter", "Simulation", "Sports", "Strategy"])
    platform = st.selectbox("Platform", ["PC", "PlayStation", "Xbox", "Nintendo", "Mobile"])
    release_year = st.number_input("Release year", min_value=2000, max_value=2035, value=2026)
    average_rating = st.number_input("Average rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
    lifecycle_status = st.selectbox("Lifecycle status", ["active", "maintenance", "sunset"])
    published_by_studio_id = st.number_input("Studio id", min_value=0, step=1, value=1)
    submitted = st.form_submit_button("Publish Game", type="primary")

if submitted:
    payload = {
        "title": title,
        "description": description,
        "genre": genre,
        "platform": platform,
        "release_year": int(release_year),
        "average_rating": average_rating,
        "lifecycle_status": lifecycle_status,
        "published_by_studio_id": None if published_by_studio_id == 0 else int(published_by_studio_id),
    }
    response, submit_error, _ = post_json("/games", payload)
    if submit_error:
        st.error(submit_error)
    else:
        st.success(f"Game created successfully with id {response['game_id']}.")

st.subheader("Recent Catalog Snapshot")
st.dataframe(
    games[:12],
    use_container_width=True,
    hide_index=True,
    column_order=["game_id", "title", "platform", "genre", "release_year", "lifecycle_status"],
)
