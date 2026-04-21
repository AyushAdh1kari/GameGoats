import streamlit as st

from modules.api_client import get_json
from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
require_persona("recommender")

st.title("Catalog Watch")
st.write("Use the live games API to spot titles with strong rating or lifecycle signals.")

games, error, _ = get_json("/games")
if error:
    st.error(error)
    st.stop()

minimum_rating = st.slider("Minimum rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
active_only = st.toggle("Show only active games", value=True)

filtered_games = []
for game in games:
    rating_match = float(game["average_rating"]) >= minimum_rating
    active_match = not active_only or game["lifecycle_status"] == "active"
    if rating_match and active_match:
        filtered_games.append(game)

st.metric("High-Signal Games", len(filtered_games))
st.dataframe(
    filtered_games,
    use_container_width=True,
    hide_index=True,
    column_order=["game_id", "title", "genre", "platform", "average_rating", "lifecycle_status"],
)
