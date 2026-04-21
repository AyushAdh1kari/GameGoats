import streamlit as st

from modules.api_client import get_json
from modules.nav import SideBarLinks
from modules.personas import require_persona, set_selected_game_id

st.set_page_config(layout="wide")
SideBarLinks()
require_persona("player")

st.title("Browse Games")
st.write("Search the live catalog coming from `GET /games`.")

games, error, _ = get_json("/games")

if error:
    st.error(error)
    st.stop()

search_term = st.text_input("Search by title", placeholder="Try Crimson, Echo, Neon, or Titan")

genres = sorted({game["genre"] for game in games})
platforms = sorted({game["platform"] for game in games})
lifecycle_states = sorted({game["lifecycle_status"] for game in games})

col1, col2, col3 = st.columns(3)
selected_genre = col1.selectbox("Genre", ["All"] + genres)
selected_platform = col2.selectbox("Platform", ["All"] + platforms)
selected_status = col3.selectbox("Lifecycle", ["All"] + lifecycle_states)

filtered_games = []
for game in games:
    title_match = search_term.lower() in game["title"].lower()
    genre_match = selected_genre == "All" or game["genre"] == selected_genre
    platform_match = selected_platform == "All" or game["platform"] == selected_platform
    status_match = selected_status == "All" or game["lifecycle_status"] == selected_status
    if title_match and genre_match and platform_match and status_match:
        filtered_games.append(game)

metric1, metric2 = st.columns(2)
metric1.metric("Matching Games", len(filtered_games))
metric2.metric("Total Catalog Size", len(games))

st.dataframe(
    filtered_games,
    use_container_width=True,
    hide_index=True,
    column_order=[
        "game_id",
        "title",
        "genre",
        "platform",
        "release_year",
        "average_rating",
        "lifecycle_status",
        "published_by_studio_name",
    ],
)

if filtered_games:
    selected_game = st.selectbox(
        "Preview a game",
        options=filtered_games,
        format_func=lambda game: f"#{game['game_id']} - {game['title']} ({game['platform']})",
    )
    st.json(selected_game)
    if st.button("Open Selected Game Details", type="primary"):
        set_selected_game_id(selected_game["game_id"])
        st.switch_page("pages/02_Player_Game_Details.py")
