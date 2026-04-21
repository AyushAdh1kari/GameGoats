import streamlit as st


def SideBarLinks(show_home=False):
    st.sidebar.image("assets/logo.png", width=150)

    if show_home:
        st.sidebar.page_link("Home.py", label="Home", icon="🏠")

    authenticated = st.session_state.get("authenticated", False)
    if not authenticated:
        return

    role = st.session_state.get("role", "")
    username = st.session_state.get("username", "")

    st.sidebar.markdown(f"**Logged in as:** {username}")
    st.sidebar.markdown(f"**Role:** {role.title()}")
    st.sidebar.divider()

    if role == "player":
        st.sidebar.page_link("pages/00_Player_Home.py", label="Player Home", icon="🎮")
        st.sidebar.page_link("pages/01_Game_Search.py", label="Game Search", icon="🔍")
        st.sidebar.page_link("pages/02_Game_Detail.py", label="Game Detail", icon="📋")
        st.sidebar.page_link("pages/03_My_Profile.py", label="My Profile", icon="👤")

    elif role == "recommender":
        st.sidebar.page_link("pages/10_Recommender_Home.py", label="Recommender Home", icon="💡")
        st.sidebar.page_link("pages/11_Recommendation_Feed.py", label="Recommendation Feed", icon="🎯")
        st.sidebar.page_link("pages/12_Game_Reviews.py", label="Game Reviews", icon="⭐")
        st.sidebar.page_link("pages/13_Forum_Threads.py", label="Forum Threads", icon="💬")

    elif role == "developer":
        st.sidebar.page_link("pages/20_Developer_Home.py", label="Developer Home", icon="🛠️")
        st.sidebar.page_link("pages/21_My_Games.py", label="My Games", icon="🎲")
        st.sidebar.page_link("pages/22_Game_Analytics.py", label="Game Analytics", icon="📊")
        st.sidebar.page_link("pages/23_Studio_Management.py", label="Studio Management", icon="🏢")

    elif role == "admin":
        st.sidebar.page_link("pages/30_Admin_Home.py", label="Admin Home", icon="🔧")
        st.sidebar.page_link("pages/31_Server_Dashboard.py", label="Server Dashboard", icon="🖥️")
        st.sidebar.page_link("pages/32_Alert_Management.py", label="Alert Management", icon="🚨")
        st.sidebar.page_link("pages/33_Report_Management.py", label="Report Management", icon="📝")

    st.sidebar.divider()
    st.sidebar.page_link("pages/40_About.py", label="About", icon="ℹ️")

    if st.sidebar.button("Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("Home.py")
