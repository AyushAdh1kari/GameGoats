from pathlib import Path

import streamlit as st


PERSONA_CONFIG = {
    "player": {
        "label": "Julia - Player",
        "role_label": "Player",
        "home": "pages/00_Player_Home.py",
        "features": [
            ("pages/01_Player_Browse_Games.py", "Browse Games"),
            ("pages/02_Player_Game_Details.py", "Game Details"),
            ("pages/03_Player_Submit_Report.py", "Submit Report"),
        ],
    },
    "developer": {
        "label": "John - Developer",
        "role_label": "Developer",
        "home": "pages/10_Developer_Home.py",
        "features": [
            ("pages/11_Developer_Publish_Game.py", "Publish Game"),
            ("pages/12_Developer_Edit_Game.py", "Edit Game"),
            ("pages/13_Developer_Retire_Game.py", "Retire Game"),
        ],
    },
    "admin": {
        "label": "Richard - System Admin",
        "role_label": "Admin",
        "home": "pages/20_Admin_Home.py",
        "features": [
            ("pages/21_Admin_Server_Dashboard.py", "Server Dashboard"),
            ("pages/22_Admin_Alert_Center.py", "Alert Center"),
            ("pages/23_Admin_Report_Console.py", "Report Console"),
        ],
    },
    "recommender": {
        "label": "Alex - Recommender",
        "role_label": "Recommender",
        "home": "pages/30_Recommender_Home.py",
        "features": [
            ("pages/31_Recommender_Catalog.py", "Catalog Watch"),
            ("pages/32_Recommender_Report_Feed.py", "Report Feed"),
            ("pages/33_Recommender_Submit_Report.py", "Safety Escalation"),
        ],
    },
}


MOCK_USERS = {
    "player": [
        {"id": 1, "display_name": "Julia Chen", "subtitle": "Favorites-driven player"},
        {"id": 9, "display_name": "Maya Lewis", "subtitle": "Weekend co-op explorer"},
        {"id": 17, "display_name": "Priya Shah", "subtitle": "Achievement hunter"},
    ],
    "developer": [
        {"id": 24, "display_name": "John Park", "subtitle": "Indie studio lead"},
        {"id": 27, "display_name": "Nina Torres", "subtitle": "Live-ops producer"},
        {"id": 33, "display_name": "Marcus Doyle", "subtitle": "Gameplay systems dev"},
    ],
    "admin": [
        {"id": 39, "display_name": "Richard Terry", "subtitle": "Primary operations admin"},
        {"id": 40, "display_name": "Dana Brooks", "subtitle": "Incident commander"},
        {"id": 37, "display_name": "Mina Hart", "subtitle": "Trust and safety lead"},
    ],
    "recommender": [
        {"id": 2, "display_name": "Alex Rivera", "subtitle": "Community curator"},
        {"id": 7, "display_name": "Sam Patel", "subtitle": "Recommendation editor"},
        {"id": 13, "display_name": "Jordan Kim", "subtitle": "Forum guide writer"},
    ],
}

APP_ROOT = Path(__file__).resolve().parents[1]


def format_mock_user(user):
    return f"{user['display_name']}  |  User #{user['id']}"


def page_exists(page_path):
    return (APP_ROOT / page_path).exists()


def get_default_user(persona_key):
    users = MOCK_USERS.get(persona_key, [])
    return users[0] if users else None


def get_available_persona_keys():
    return [
        persona_key
        for persona_key, persona in PERSONA_CONFIG.items()
        if page_exists(persona["home"])
    ]


def get_available_personas():
    return {
        persona_key: PERSONA_CONFIG[persona_key]
        for persona_key in get_available_persona_keys()
    }


def get_available_features(persona_key):
    return [
        (page_path, page_label)
        for page_path, page_label in PERSONA_CONFIG[persona_key]["features"]
        if page_exists(page_path)
    ]


def login_as(persona_key, user):
    st.session_state["mock_user"] = {
        **user,
        "persona": persona_key,
        "persona_label": PERSONA_CONFIG[persona_key]["label"],
        "role_label": PERSONA_CONFIG[persona_key]["role_label"],
        "home": PERSONA_CONFIG[persona_key]["home"],
    }


def logout():
    st.session_state.pop("mock_user", None)


def get_current_user():
    return st.session_state.get("mock_user")


def get_selected_game_id():
    return st.session_state.get("selected_game_id")


def set_selected_game_id(game_id):
    st.session_state["selected_game_id"] = game_id


def require_persona(persona_key):
    user = get_current_user()
    if not user:
        default_user = get_default_user(persona_key)
        if default_user:
            login_as(persona_key, default_user)
            return get_current_user()

        st.warning("No mock users are configured for this persona.")
        if st.button("Return to Home", type="primary"):
            st.switch_page("Home.py")
        st.stop()

    if user["persona"] != persona_key:
        expected_label = PERSONA_CONFIG[persona_key]["label"]
        st.warning(f"This page is for {expected_label}. You are logged in as {user['persona_label']}.")
        if st.button("Go To My Home", type="primary"):
            if page_exists(user["home"]):
                st.switch_page(user["home"])
            else:
                st.switch_page("Home.py")
        st.stop()

    return user
