import streamlit as st

from modules.api_client import get_json
from modules.nav import SideBarLinks
from modules.personas import get_selected_game_id, require_persona, set_selected_game_id

st.set_page_config(layout="wide")
SideBarLinks()
require_persona("player")

st.title("Game Details")
st.write("Inspect one game at a time through `GET /games/<game_id>`.")

games, error, _ = get_json("/games")
if error:
    st.error(error)
    st.stop()

default_game_id = get_selected_game_id() or games[0]["game_id"]
default_index = next(
    (index for index, game in enumerate(games) if game["game_id"] == default_game_id),
    0,
)

selected_game = st.selectbox(
    "Select a game",
    options=games,
    index=default_index,
    format_func=lambda game: f"#{game['game_id']} - {game['title']} ({game['platform']})",
)
set_selected_game_id(selected_game["game_id"])

game_detail, detail_error, _ = get_json(f"/games/{selected_game['game_id']}")
if detail_error:
    st.error(detail_error)
    st.stop()

metric1, metric2, metric3 = st.columns(3)
metric1.metric("Average Rating", game_detail["average_rating"])
metric2.metric("Release Year", game_detail["release_year"])
metric3.metric("Lifecycle", game_detail["lifecycle_status"])

left, right = st.columns([2, 1])

with left:
    st.subheader(game_detail["title"])
    st.write(game_detail["description"])
    st.write(f"Genre: `{game_detail['genre']}`")
    st.write(f"Platform: `{game_detail['platform']}`")
    st.write(f"Published By Studio: `{game_detail['published_by_studio_name']}`")

with right:
    st.subheader("Raw API Payload")
    st.json(game_detail)
