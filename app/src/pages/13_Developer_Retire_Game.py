import streamlit as st

from modules.api_client import delete_json, get_json
from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
require_persona("developer")

st.title("Retire Game")
st.write("Delete a game from the catalog using `DELETE /games/<game_id>`.")

games, error, _ = get_json("/games")
if error:
    st.error(error)
    st.stop()

selected_game = st.selectbox(
    "Select a game to remove",
    options=games,
    format_func=lambda game: f"#{game['game_id']} - {game['title']} ({game['platform']})",
)

st.warning("This action deletes the selected game record from the live API.")
st.json(selected_game)

confirm_delete = st.checkbox("I understand this will delete the selected game.")
if st.button("Delete Game", type="primary", disabled=not confirm_delete):
    response, delete_error, _ = delete_json(f"/games/{selected_game['game_id']}")
    if delete_error:
        st.error(delete_error)
    else:
        st.success(response["message"])
