import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="My Profile", page_icon="👤")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "player":
    st.warning("Please log in as a Player from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]
username = st.session_state["username"]

st.title("My Profile")

try:
    resp = requests.get(f"{API}/users/{user_id}", timeout=5)
    user = resp.json() if resp.status_code == 200 else {}
except Exception:
    user = {}

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown(f"### {username}")
    st.markdown(f"**Region:** {user.get('region', '–')}")
    st.markdown(f"**Member since:** {str(user.get('created_at', '–'))[:10]}")

with col2:
    c1, c2, c3 = st.columns(3)
    try:
        favs_resp = requests.get(f"{API}/users/{user_id}/favorites", timeout=5)
        favorites = favs_resp.json() if favs_resp.status_code == 200 else []
    except Exception:
        favorites = []
    c1.metric("Favorites", len(favorites))

    try:
        comments_resp = requests.get(f"{API}/users/{user_id}/comments", timeout=5)
        comments = comments_resp.json() if comments_resp.status_code == 200 else []
    except Exception:
        comments = []
    c2.metric("Reviews", len(comments))

    try:
        follows_resp = requests.get(f"{API}/users/{user_id}/follows", timeout=5)
        follows = follows_resp.json() if follows_resp.status_code == 200 else []
    except Exception:
        follows = []
    c3.metric("Following", len(follows))

st.divider()

st.subheader("My Favorites")
if favorites:
    for f in favorites:
        with st.container(border=True):
            fc1, fc2, fc3 = st.columns([4, 2, 1])
            with fc1:
                game_title = f.get("title", f"Game #{f.get('game_id', '?')}")
                st.markdown(f"**{game_title}**")
            with fc2:
                st.caption(f"Priority: {f.get('priority', '–')}")
            with fc3:
                if st.button("Remove", key=f"rm_fav_{f.get('favorite_id', f.get('game_id'))}",
                             use_container_width=True):
                    try:
                        del_resp = requests.delete(
                            f"{API}/users/{user_id}/favorites/{f['game_id']}",
                            timeout=5,
                        )
                        if del_resp.status_code == 200:
                            st.success("Removed from favorites.")
                            st.rerun()
                        else:
                            st.error(f"Failed: {del_resp.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
else:
    st.info("You haven't added any favorites yet.")

st.divider()

st.subheader("Following")
if follows:
    cols = st.columns(4)
    for i, f in enumerate(follows):
        with cols[i % 4]:
            name = f.get("username", f"User #{f.get('followed_user_id', '?')}")
            st.markdown(f"**{name}**")
else:
    st.info("You aren't following anyone yet.")
