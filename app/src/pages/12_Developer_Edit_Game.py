import streamlit as st

from modules.api_client import get_json, put_json
from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
require_persona("developer")

st.title("Edit Game")
st.write("Update an existing title with `PUT /games/<game_id>`.")

games, error, _ = get_json("/games")
if error:
    st.error(error)
    st.stop()

selected_game = st.selectbox(
    "Select a game to edit",
    options=games,
    format_func=lambda game: f"#{game['game_id']} - {game['title']} ({game['platform']})",
)

platform_options = ["PC", "PlayStation", "Xbox", "Nintendo", "Mobile"]
lifecycle_options = ["active", "maintenance", "sunset"]

with st.form("edit_game_form"):
    title = st.text_input("Title", value=selected_game["title"])
    description = st.text_area("Description", value=selected_game["description"])
    genre = st.text_input("Genre", value=selected_game["genre"])
    platform = st.selectbox(
        "Platform",
        platform_options,
        index=platform_options.index(selected_game["platform"]),
    )
    release_year = st.number_input(
        "Release year",
        min_value=2000,
        max_value=2035,
        value=int(selected_game["release_year"]),
    )
    average_rating = st.number_input(
        "Average rating",
        min_value=0.0,
        max_value=5.0,
        value=float(selected_game["average_rating"]),
        step=0.1,
    )
    lifecycle_status = st.selectbox(
        "Lifecycle status",
        lifecycle_options,
        index=lifecycle_options.index(selected_game["lifecycle_status"]),
    )
    published_by_studio_id = st.number_input(
        "Studio id",
        min_value=0,
        step=1,
        value=int(selected_game["published_by_studio_id"] or 0),
    )
    submitted = st.form_submit_button("Save Changes", type="primary")

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
    response, submit_error, _ = put_json(f"/games/{selected_game['game_id']}", payload)
    if submit_error:
        st.error(submit_error)
    else:
        st.success(response["message"])

st.subheader("Selected Game Payload")
st.json(selected_game)
