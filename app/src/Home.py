import streamlit as st

st.set_page_config(layout="wide", page_title="GameGoats", page_icon="🐐")

from modules.nav import SideBarLinks

SideBarLinks(show_home=True)

st.image("assets/logo.png", width=280)
st.write("")

st.markdown("#### Select a role and user to get started")

API = "http://web-api:4000"

ROLE_USERS = {
    "Player": [
        {"user_id": 1, "username": "johnsonjoshua91"},
        {"user_id": 2, "username": "yherrera41"},
        {"user_id": 3, "username": "richard1396"},
        {"user_id": 4, "username": "ryan7014"},
        {"user_id": 5, "username": "samuel8739"},
    ],
    "Recommender": [
        {"user_id": 10, "username": "nicolejohnson53"},
        {"user_id": 15, "username": "dayderek34"},
        {"user_id": 20, "username": "tkerr87"},
        {"user_id": 25, "username": "fmcguire30"},
        {"user_id": 29, "username": "manuel1291"},
    ],
    "Developer": [
        {"user_id": 24, "username": "toni1824"},
        {"user_id": 26, "username": "alexis8295"},
        {"user_id": 30, "username": "andrea8617"},
        {"user_id": 33, "username": "steve0760"},
        {"user_id": 36, "username": "vaughnjeff64"},
    ],
    "Admin": [
        {"user_id": 39, "username": "willisanna90"},
        {"user_id": 40, "username": "vjones86"},
    ],
}

ROLE_PAGES = {
    "Player": "pages/00_Player_Home.py",
    "Recommender": "pages/10_Recommender_Home.py",
    "Developer": "pages/20_Developer_Home.py",
    "Admin": "pages/30_Admin_Home.py",
}

col1, col2, col3, col4 = st.columns(4)
cols = [col1, col2, col3, col4]

for i, (role, users) in enumerate(ROLE_USERS.items()):
    with cols[i]:
        st.subheader(role)
        user_options = {u["username"]: u for u in users}
        selected_name = st.selectbox(
            f"Select {role} user",
            options=list(user_options.keys()),
            key=f"select_{role}",
        )
        if st.button(f"Login as {role}", type="primary", use_container_width=True, key=f"btn_{role}"):
            chosen = user_options[selected_name]
            st.session_state["authenticated"] = True
            st.session_state["role"] = role.lower()
            st.session_state["user_id"] = chosen["user_id"]
            st.session_state["username"] = chosen["username"]
            st.switch_page(ROLE_PAGES[role])
