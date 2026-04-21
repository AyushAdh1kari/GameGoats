import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

st.write("# About GameGoats")
st.markdown(
    """
    GameGoats is a multi-persona platform for browsing games, publishing titles,
    monitoring safety signals, and managing live operations.

    ### Where the project is now

    The frontend has moved beyond the original setup-only pages and now focuses on
    persona-driven demo flows. The Streamlit app currently supports four active personas:
    player, developer, recommender, and admin.

    ### What is working in this branch

    - mock login from the landing page using seeded demo users
    - player pages for browsing the game catalog, inspecting game details, and filing reports
    - developer pages for creating, editing, and deleting games
    - admin pages for reviewing servers, managing alerts, and processing reports
    - recommender pages for tracking the catalog and submitting safety escalations
    - container/API/database health checks from the Streamlit app

    ### Current backend coverage

    Live Flask routes in use here include:
    - system health routes
    - full CRUD for `games`
    - admin routes for `reports`, `servers`, and `alerts`

    The remaining `users/recommendations` and `studio_developer/community` backend areas
    are still being wired up, so this app branch is intentionally centered on the APIs
    that are already live and testable.
    """
)

if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
