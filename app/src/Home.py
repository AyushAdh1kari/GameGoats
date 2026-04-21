import streamlit as st

from modules.nav import SideBarLinks
from modules.personas import (
    MOCK_USERS,
    format_mock_user,
    get_available_personas,
    get_current_user,
    login_as,
)

st.set_page_config(layout="wide")
SideBarLinks(show_home=True)

st.title("GameGoats")
st.write("Choose a persona, pick a mock user, and jump into the live GameGoats demo flows.")

active_user = get_current_user()
if active_user:
    st.info(
        f"Current session: {active_user['display_name']} "
        f"({active_user['persona_label']}, User #{active_user['id']})"
    )

available_personas = get_available_personas()
persona_order = [
    persona_key
    for persona_key in ["player", "developer", "recommender", "admin"]
    if persona_key in available_personas
]
columns = st.columns(2)

for index, persona_key in enumerate(persona_order):
    persona = available_personas[persona_key]
    users = MOCK_USERS[persona_key]

    with columns[index % 2]:
        st.subheader(persona["label"])
        st.caption(f"Mock {persona['role_label'].lower()} profiles for demo navigation.")
        selected_user = st.selectbox(
            f"Select a {persona['role_label'].lower()}",
            options=users,
            format_func=format_mock_user,
            key=f"{persona_key}_selector",
        )
        if st.button(f"Login As {selected_user['display_name']}", type="primary", use_container_width=True):
            login_as(persona_key, selected_user)
            st.switch_page(persona["home"])

st.divider()
st.subheader("Live API Features In This Branch")

left, right = st.columns(2)

with left:
    st.markdown(
        """
        - Player browsing and game detail views
        - Developer game publishing, editing, and retirement flows
        - Recommender catalog watch plus report submission tools
        """
    )

with right:
    st.markdown(
        """
        - Admin server dashboard
        - Admin alert management
        - Admin report console
        """
    )
