import base64
from pathlib import Path

import streamlit as st

from modules.personas import (
    get_default_user,
    get_available_features,
    get_available_personas,
    get_current_user,
    login_as,
    logout,
    page_exists,
)


def _render_home_logo():
    logo_path = Path(__file__).resolve().parents[1] / "assets" / "logo.png"
    encoded_logo = base64.b64encode(logo_path.read_bytes()).decode("ascii")

    st.sidebar.markdown(
        f"""
        <style>
        .gamegoats-home-logo {{
            display: block;
            width: 160px;
            margin: 0 auto 0.35rem auto;
            border-radius: 18px;
            overflow: hidden;
            transform: translateY(0);
            transition: transform 160ms ease, box-shadow 160ms ease, filter 160ms ease;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.16);
        }}
        .gamegoats-home-logo:hover {{
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 18px 34px rgba(15, 23, 42, 0.24);
            filter: saturate(1.04);
        }}
        .gamegoats-home-logo img {{
            display: block;
            width: 100%;
        }}
        .gamegoats-home-caption {{
            text-align: center;
            font-size: 0.82rem;
            color: rgba(49, 51, 63, 0.78);
            margin-bottom: 0.4rem;
        }}
        </style>
        <a class="gamegoats-home-logo" href="/" target="_self" title="Return to Home">
            <img src="data:image/png;base64,{encoded_logo}" alt="GameGoats Home" />
        </a>
        <div class="gamegoats-home-caption">Return Home</div>
        """,
        unsafe_allow_html=True,
    )


def SideBarLinks(show_home=False):
    """
    Display the sidebar with links to different pages of the GameGoats application.

    Args:
        show_home (bool): Whether to show the Home link in the sidebar. Default is False

    Returns:
        None
    """
    _render_home_logo()

    user = get_current_user()

    if user:
        st.sidebar.caption(f"Logged in as {user['display_name']}")
        st.sidebar.write(f"{user['persona_label']}  |  ID {user['id']}")
        st.sidebar.caption(user["subtitle"])
        if st.sidebar.button("Log Out", use_container_width=True):
            logout()
            st.switch_page("Home.py")

        st.sidebar.divider()
        st.sidebar.subheader("My Workspace")
        persona_config = get_available_personas().get(user["persona"])
        if persona_config and page_exists(persona_config["home"]):
            st.sidebar.page_link(persona_config["home"], label=f"{persona_config['role_label']} Home")
        for page_path, page_label in get_available_features(user["persona"]):
            st.sidebar.page_link(page_path, label=page_label)
    else:
        st.sidebar.subheader("Persona Access")
        st.sidebar.caption("Use a quick-enter button to log in as the default mock user for that role.")
        for persona_key, persona in get_available_personas().items():
            if st.sidebar.button(persona["label"], use_container_width=True, key=f"enter_{persona_key}"):
                default_user = get_default_user(persona_key)
                if default_user:
                    login_as(persona_key, default_user)
                    st.switch_page(persona["home"])

    st.sidebar.divider()
    st.sidebar.subheader("Project Setup")
    setup_pages = [
        ("pages/14_Container_Status.py", "Container Status"),
        ("pages/30_About.py", "About"),
    ]
    for page_path, page_label in setup_pages:
        if page_exists(page_path):
            st.sidebar.page_link(page_path, label=page_label)
