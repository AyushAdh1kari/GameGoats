import requests
import streamlit as st

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Game Reviews", page_icon="⭐")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "recommender":
    st.warning("Please log in as a Recommender from the Home page.")
    st.stop()

API = "http://web-api:4000"
user_id = st.session_state["user_id"]

st.title("Game Reviews")

try:
    resp = requests.get(f"{API}/games", timeout=5)
    all_games = resp.json() if resp.status_code == 200 else []
except Exception:
    all_games = []

game_options = {g["title"]: g["game_id"] for g in all_games}
selected_title = st.selectbox("Select a game to review", list(game_options.keys()))
game_id = game_options.get(selected_title)

if not game_id:
    st.info("No games available.")
    st.stop()

st.divider()

st.subheader("Write a Review")
with st.form("rec_review_form", clear_on_submit=True):
    review_rating = st.slider("Rating", 1, 5, 3)
    review_text = st.text_area("Your review", max_chars=500,
                               placeholder="Share your thoughts to help inform recommendations...")
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
                st.error(f"Failed: {resp.text}")
        except Exception as e:
            st.error(f"API error: {e}")
    elif submitted:
        st.warning("Please write something before submitting.")

st.divider()

st.subheader(f"All Reviews for {selected_title}")
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
    st.info("No reviews yet for this game.")
