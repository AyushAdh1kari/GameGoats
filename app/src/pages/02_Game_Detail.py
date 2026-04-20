import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Game Detail", page_icon="📋")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "player":
    st.warning("Please log in as a Player from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]

try:
    resp = requests.get(f"{API}/games", timeout=5)
    all_games = resp.json() if resp.status_code == 200 else []
except Exception:
    all_games = []

game_options = {g["title"]: g["game_id"] for g in all_games}
preselect = st.session_state.get("selected_game_id")
default_idx = 0
if preselect:
    ids = list(game_options.values())
    if preselect in ids:
        default_idx = ids.index(preselect)

selected_title = st.selectbox("Select a game", list(game_options.keys()), index=default_idx)
game_id = game_options.get(selected_title)

if not game_id:
    st.info("No games available.")
    st.stop()

try:
    game = requests.get(f"{API}/games/{game_id}", timeout=5).json()
except Exception:
    st.error("Could not load game details.")
    st.stop()

st.title(game.get("title", ""))
rating = game.get("average_rating", 0)
if isinstance(rating, str):
    rating = float(rating)

col1, col2, col3 = st.columns(3)
col1.markdown(f"**Genre:** {game.get('genre', '–')}")
col2.markdown(f"**Platform:** {game.get('platform', '–')}")
col3.markdown(f"**Rating:** ⭐ {rating:.1f}")

st.markdown(f"**Status:** {game.get('lifecycle_status', '–')} · **Release Year:** {game.get('release_year', '–')}")
st.markdown(game.get("description", ""))

try:
    tag_resp = requests.get(f"{API}/games/{game_id}/tags", timeout=5)
    tags = tag_resp.json() if tag_resp.status_code == 200 else []
    if tags:
        tag_str = "  ".join([f"`{t['tag_name']}`" for t in tags])
        st.markdown(f"**Tags:** {tag_str}")
except Exception:
    pass

st.divider()

st.subheader("Write a Review")
with st.form("review_form", clear_on_submit=True):
    review_rating = st.slider("Rating", 1, 5, 3)
    review_text = st.text_area("Your review", max_chars=500)
    submitted = st.form_submit_button("Submit Review", type="primary")
    if submitted and review_text.strip():
        try:
            resp = requests.post(
                f"{API}/games/{game_id}/comments",
                json={
                    "created_by_user_id": user_id,
                    "comment_text": review_text.strip(),
                    "rating": review_rating,
                },
                timeout=5,
            )
            if resp.status_code == 201:
                st.success("Review submitted!")
                st.rerun()
            else:
                st.error(f"Failed to submit: {resp.text}")
        except Exception as e:
            st.error(f"API error: {e}")
    elif submitted:
        st.warning("Please write something before submitting.")

st.subheader("Reviews")
try:
    comments_resp = requests.get(f"{API}/games/{game_id}/comments", timeout=5)
    comments = comments_resp.json() if comments_resp.status_code == 200 else []
except Exception:
    comments = []

if comments:
    for c in comments:
        with st.container(border=True):
            r = c.get("rating", 0)
            stars = "⭐" * int(r)
            st.markdown(f"**User #{c.get('created_by_user_id', '?')}** {stars}")
            st.write(c.get("comment_text", ""))
            st.caption(f"Posted: {c.get('created_at', '–')}")
else:
    st.info("No reviews yet. Be the first!")

st.divider()

st.subheader("Discussion Forum")
try:
    threads_resp = requests.get(f"{API}/games/{game_id}/forum-threads", timeout=5)
    threads = threads_resp.json() if threads_resp.status_code == 200 else []
except Exception:
    threads = []

if threads:
    for t in threads:
        with st.container(border=True):
            st.markdown(f"**{t.get('title', 'Untitled Thread')}**")
            st.caption(f"By User #{t.get('created_by_user_id', '?')} · {t.get('created_at', '–')}")
else:
    st.info("No forum threads for this game yet.")
