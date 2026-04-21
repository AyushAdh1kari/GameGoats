import streamlit as st

from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
user = require_persona("developer")

st.title("John Developer Home")
st.write(
    f"Welcome, {user['display_name']}. This workspace covers the live game publishing and maintenance routes."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Publish Game")
    st.caption("Create a new game record with the live `POST /games` endpoint.")
    if st.button("Open Publish Flow", type="primary", use_container_width=True):
        st.switch_page("pages/11_Developer_Publish_Game.py")

with col2:
    st.subheader("Edit Game")
    st.caption("Select a title, tweak metadata, and push updates through `PUT /games/<game_id>`.")
    if st.button("Open Edit Flow", type="primary", use_container_width=True):
        st.switch_page("pages/12_Developer_Edit_Game.py")

with col3:
    st.subheader("Retire Game")
    st.caption("Delete a title from the catalog to exercise `DELETE /games/<game_id>`.")
    if st.button("Open Retirement Flow", type="primary", use_container_width=True):
        st.switch_page("pages/13_Developer_Retire_Game.py")

st.divider()
st.markdown(
    """
    ### Developer demo flow
    1. Publish a new game.
    2. Edit it in place.
    3. Remove it when you are done testing.
    """
)
