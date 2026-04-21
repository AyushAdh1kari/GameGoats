import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="About", page_icon="ℹ️")
SideBarLinks(show_home=True)

st.image("assets/logo.png", width=200)
st.write("")

st.title("About GameGoats")

st.markdown(
    """
    **GameGoats** is a gaming community platform for discovering, reviewing, and
    managing games. The platform serves four distinct user roles:

    - **Players** — Search and browse games, write reviews, manage favorites,
      and connect with other players.
    - **Recommenders** — Curate game recommendations, review titles, and
      participate in community forum discussions.
    - **Developers** — Publish games, track analytics and ratings, and manage
      studio profiles.
    - **Admins** — Monitor server infrastructure, manage alerts and incidents,
      and handle community reports.

    ### Tech Stack

    | Layer | Technology |
    |-------|-----------|
    | Frontend | Streamlit |
    | API | Flask (Python) |
    | Database | MySQL 8.4 |
    | Infrastructure | Docker Compose |
    """
)

if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
